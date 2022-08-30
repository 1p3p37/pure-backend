from json import dumps as json_dumps

from django.conf import settings

from crosschain_backend.consts import (
    ALTERNATIVE_DEFAULT_CRYPTO_ADDRESS,
    DEFAULT_CRYPTO_ADDRESS,
)
from networks.models import TradeParams
from networks.services.near_api.account import Account
from networks.services.near_api.providers import JsonProvider
from networks.services.near_api.signer import Signer, KeyPair


def get_ref_finance_pool_count(account: Account) -> int:
    response = account.view_function(
        contract_id='v2.ref-finance.near',
        method_name='get_number_of_pools',
    )

    return response.get('result')


def get_ref_finance_pools(
    account: Account,
    from_index: int = 0,
    limit: int = 100,
) -> list:
    response = account.view_function(
        contract_id='v2.ref-finance.near',
        method_name='get_pools',
        args={
            'from_index': from_index,
            'limit': limit,
        }
    )

    return response.get('result')


def get_ref_finance_pool_ids(
    account: Account,
    path: list,
    pool_index: int = 0,
    limit: int = 100,
):
    if len(path) == 1:
        return []

    total_ref_finance_pool_count = get_ref_finance_pool_count(
        account=account
    )

    if not total_ref_finance_pool_count:
        raise Exception('Near pools in v2.ref-finance.near not found')

    pool_ids_list = list()

    while 1:
        if pool_index > total_ref_finance_pool_count:
            break

        pools = get_ref_finance_pools(
            account=account,
            from_index=pool_index,
            limit=limit,
        )

        for counter, pool in enumerate(pools):
            if path != pool.get('token_account_ids'):
                continue

            pool_ids_list.append(counter + pool_index)

            continue

        pool_index += limit

        continue

    return pool_ids_list


def create_token_account(
    account: Account,
    token_list: list,
    wallet_address: str
):
    """
    Creates token account for user's wallet if it's not already exist
    It's necessary for successful transaction.
    """

    for token_address in token_list:
        if token_address == 'near':
            continue

        # READ function call method
        result = account.view_function(
            contract_id=token_address,
            method_name='storage_balance_of',
            args={
                'account_id': wallet_address,
            }
        )

        if result['result']:
            continue

        # WRIGHT function call method
        account.function_call(
            contract_id=token_address,
            method_name='storage_deposit',
            args={
                'account_id': wallet_address,
            },
            amount=int(account.view_function(
                contract_id=token_address,
                method_name='storage_balance_bounds',
                args={
                    'account_id': wallet_address,
                }
            )['result']['max']),
        )


def build_and_send_transaction_near(
    trade,
    contract,
    wallet_address,
    transit_token_amount_in,
    token_out_min,
    original_tx_hash,
    network,
    second_path,
):
    trade_params = TradeParams.objects \
        .filter(
            from_tx_hash__iexact=trade.from_onchain_swap
            .transaction.hash,
            from_network=trade.from_onchain_swap.contract.network,
        ) \
        .first()

    if wallet_address in (
        DEFAULT_CRYPTO_ADDRESS.lower(),
        ALTERNATIVE_DEFAULT_CRYPTO_ADDRESS.lower(),
    ):
        wallet_address = trade_params.json_data.get('walletAddress')

    if DEFAULT_CRYPTO_ADDRESS in second_path:
        second_path = trade_params.json_data.get('secondPath')

    rpc_provider = JsonProvider(
        rpc_addr=network.rpc_url_list[0],
    )

    key_pair = KeyPair(
        secret_key=settings.NEAR_PRIVATE_KEY,
    )

    signer = Signer(
        account_id=settings.RELAYER_NEAR_ACCOUNT_ID,
        key_pair=key_pair,
    )

    # All actions(contract calls) needs to be done with Account instance
    account = Account(
        provider=rpc_provider,
        signer=signer,
        account_id=settings.RELAYER_NEAR_ACCOUNT_ID,
    )

    create_token_account(
        account=account,
        token_list=second_path,
        wallet_address=wallet_address,
    )

    args = {
        "params": {
            "new_address": wallet_address,
            "token_out": second_path[-1],
            "amount_in_with_fee": str(transit_token_amount_in),
            "amount_out_min": str(token_out_min),
            "original_tx_hash": original_tx_hash,
        },
    }

    if len(second_path) > 1:
        # For token path greater than 1 necessary to make a list of pools
        # and put it in "msg"
        trade_params = TradeParams.objects \
            .filter(
                from_tx_hash__iexact=trade.from_onchain_swap
                .transaction.hash,
                from_network=trade.from_onchain_swap.contract.network,
            ) \
            .first()

        if not trade_params:
            pool_ids = get_ref_finance_pool_ids(
                account=account,
                path=second_path,
            )
        else:
            pool_ids = trade_params.json_data.get('pool')

        pool_list = list(
            {
                "pool_id": pool_ids[i],
                "token_in": second_path[0],
                "token_out": second_path[-1],
                "min_amount_out": str(0),
            }
            for i in range(len(pool_ids))
        )

        pool_list[0].update({'amount_in': str(transit_token_amount_in)})
        pool_list[-1].update({'min_amount_out': str(token_out_min)})

        args.update(
            {
                "msg": json_dumps(
                    {
                        "force": 0,
                        "actions": pool_list,
                    }
                )
            }
        )

    result = account.function_call(
        contract_id=contract.address,
        method_name='swap_tokens_to_user_with_fee',
        args=args,
    )

    return result['transaction']['hash']
