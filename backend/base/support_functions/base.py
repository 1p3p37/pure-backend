from decimal import Decimal, ROUND_HALF_UP
from logging import info
from time import sleep
from typing import Union

from base58 import b58encode as base58_encode

from django.conf import settings

from requests import get as request_get

from rest_framework.status import HTTP_200_OK

from web3 import Web3

from base.support_functions.requests import send_get_request  # noqa: I100

from contracts.exceptions import ContractTestCallError

from crosschain_backend.consts import (
    COINGECKO_API_URL,
    COINGECKO_NETWORKS_NAME,
    DEFAULT_FIAT_CURRENCY_DECIMALS,
    INCH_API_URL,
    INCH_NETWORKS_ID,
    RELAYER_API_URL,
    RUBIC_BACKEND_API_URL,
)


NUM_OF_REQUESTS = 30
TIMEOUT_REQUEST = 3


def round_fiat_decimals(value: Union[Decimal, float]) -> Decimal:
    """
    Rounds input value by rules for fiat currency.

    :param value: value to be rounded
    :type value: Union[Decimal, float]
    :return: rounded value
    :rtype: Decimal
    """
    return Decimal(value).quantize(
        Decimal(f'1.{"0" * DEFAULT_FIAT_CURRENCY_DECIMALS}'),
        ROUND_HALF_UP
    )


def camel_case_split(string: str) -> str:
    """
    Converts camel case string to normal string
    """

    string_list = [string[0]]

    for ch in string[1:]:
        if ch.isupper():
            string_list.append(ch)
        else:
            string_list[-1] += ch

    return ' '.join(string_list)


def get_coingecko_token_data(token_address: str, network: str):
    response = request_get(COINGECKO_API_URL.format(
        network=COINGECKO_NETWORKS_NAME.get(network, ''),
        token_address=token_address.lower(),
    ))

    if response.status_code == HTTP_200_OK:
        return response.json()


def bytes_to_base58(string: str):
    if not string.startswith('0x'):
        return string

    return base58_encode(Web3.toBytes(hexstr=string)).decode('utf-8')


def bytearray_to_base58(byte_list):
    return base58_encode(bytes(byte_list)).decode()


def bytes_to_bytearray(byte_string):
    """
    Converts bytestring to bytearray
    """

    return [byte for byte in byte_string]


def get_token_data(token_address: str, network: str):
    token_data = request_get(
        RUBIC_BACKEND_API_URL.format(
            main_backend_url=settings.MAIN_BACKEND,
            network=network,
            token_address=token_address,
        )
    ) \
        .json()

    if not token_data:
        return
    else:
        return token_data[0]


def get_coingecko_token_usd_price(token_address: str, network: str):
    token_data = get_coingecko_token_data(token_address, network)

    if not token_data:
        token_data = get_token_data(
            token_address=token_address,
            network=network,
        )

        return token_data.get('usd_price', 0) or 0

    return token_data \
        .get('market_data', {}) \
        .get('current_price', {}) \
        .get('usd', 0)


def get_trade_params(from_tx_hash: str, network: str) -> dict:
    return send_get_request(
        RELAYER_API_URL.format(
            relayer_url=settings.RELAYER_URL,
            network=network,
            from_tx_hash=from_tx_hash,
        )
    )


def get_inch_slippage(
    network_name,
    path,
    transit_token_amount_in,
    token_out_min,
    original_tx_hash,
):
    params = {
        'fromTokenAddress': path[0],
        'toTokenAddress': path[-1],
        'amount': transit_token_amount_in,
    }

    response = send_get_request(
        url=INCH_API_URL.format(
            network_id=INCH_NETWORKS_ID.get(network_name),
            endpoint_type='quote',
        ),
        params=params,
    )

    info(f'1Inch quote response for \"{original_tx_hash}\": \"{response}\".')

    if not response:
        return 1

    to_token_amount = int(response.get('toTokenAmount', token_out_min))

    slippage = int(
        (abs(to_token_amount - token_out_min) / to_token_amount) * 100
    )

    max_oneinch_slippage = 50

    if slippage >= max_oneinch_slippage:
        raise ContractTestCallError(
            # TODO: Сделать кастомное исключение для 1inch.
            'Slippage limit exceeded when trading in 1inch.'
            f' Calculated slippage: \"{slippage}\".'
            f' Max slippage: \"{max_oneinch_slippage}\".'
        )

    return int(slippage)


def get_inch_data(
    contract_address,
    network_name,
    path,
    transit_token_amount_in,
    token_out_min,
    new_address,
    original_tx_hash
):
    if not isinstance(original_tx_hash, str):
        original_tx_hash = original_tx_hash.hex()

    info(f'Request to 1inch API for \"{original_tx_hash}\" hash.')

    params = {
        'fromTokenAddress': path[0],
        'toTokenAddress': path[-1],
        'amount': transit_token_amount_in,
        'fromAddress': contract_address,
        'slippage': get_inch_slippage(
            network_name=network_name,
            path=path,
            transit_token_amount_in=transit_token_amount_in,
            token_out_min=token_out_min,
            original_tx_hash=original_tx_hash,
        ),
        'destReceiver': new_address,
        'disableEstimate': 'true',
    }

    response = send_get_request(
        url=INCH_API_URL.format(
            network_id=INCH_NETWORKS_ID.get(network_name),
            endpoint_type='swap',
        ),
        params=params,
    )

    info(f'1Inch swap response for \"{original_tx_hash}\": {response}.')

    count = 0

    if not response:
        while count < NUM_OF_REQUESTS:
            info(f'{params=}')

            response = send_get_request(
                url=INCH_API_URL.format(
                    network_id=INCH_NETWORKS_ID.get(network_name),
                    endpoint_type='swap',
                ),
                params=params,
            )

            if response:
                break

            count += 1
            sleep(TIMEOUT_REQUEST)
        else:
            return response

    return response.get('tx', {}).get('data', '')
