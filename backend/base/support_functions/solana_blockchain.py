from base64 import b64decode as base64_decode
from json import loads as json_loads
from logging import exception, info
from time import sleep

from borsh_construct import (
    Bool,
    CStruct,
    U128,
    U64,
    U8,
)

from construct.lib.containers import ListContainer

from django.conf import settings

from requests.exceptions import ConnectionError as RequestsConnectionError

from solana.blockhash import Blockhash
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
from solana.rpc.core import (
    UnconfirmedTxError as SolanaUnconfirmedTxError,
)
from solana.rpc.types import TxOpts as SolanaTxnOpts
from solana.system_program import SYS_PROGRAM_ID
from solana.transaction import (
    AccountMeta,
    Transaction,
    TransactionInstruction,
)

from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address

from web3 import Web3

from crosschain_backend.consts import (  # noqa: I100
    RAYDIUM_POOL_API_URL,
    REQUEST_ERROR,
    SOLANA_NATIVE_TOKEN_ADDRESS,
    SOLANA_TRANSFER_TOKEN_ADDRESS,
    TRANSACTION_ERROR,
)

from networks.models import Network

from trades.exceptions import TradeError

from .base import bytearray_to_base58, bytes_to_bytearray
from .requests import send_get_request

PREFIX = 'rubic'
CONFIG = 'config'
TRANSACTION = 'transaction'
INSTRUCTION_NUMBER = 0

PROGRAM_ID = PublicKey('r2TGRLHRtQ2Uj1CR7TCBYKgRxJi5M8FRjcqZnyQzYDB')
LIQUIDITY_POOL_PROGRAM_ID_V4 = '675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8'
SERUM_PROGRAM_ID_V3 = '9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin'
SERUM_CONST = '461R7gK9GK1kLUXQbHgaW9L6PESQFSLGxKXahvcHEJwD'
VERSION = 0

RELAYER_PUBLIC_KEY = PublicKey('AymVirfHmig57eTNB86Hrg6YpJNikmNqTx35LpTCdZ65')
VALIDATOR_PUBLIC_KEY = PublicKey(
    'Fsz7qF8KobAb8mdtRAXQ8apmEXC44am6Sh13qVEwfW2m'
)
SOLANA_WRAPPED_TOKEN_ADDRESS = 'So11111111111111111111111111111111111111112'
PDA_WRAPPED = PublicKey(
    '6jVSCbM1MVZWCSepdBXY65U4uszY7rY6Lm3oEU5ZeE7q'
)
AMM_AUTHORITY = '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1'

TRANSFER_DATA_TYPE = {
    SOLANA_TRANSFER_TOKEN_ADDRESS: 1,
    SOLANA_NATIVE_TOKEN_ADDRESS: 2,
}
NOT_TRANSFER_TOKEN_TYPE = 0
TRANSFER_TOKEN_TYPE = 1
NATIVE_TOKEN_TYPE = 2

# Hardcoded data for Solana pools
# TODO: Move it to json file
SERUM_POOLS = {
    '58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2': {  # SOL-USDC
        'serumAsks': 'CEQdAFKdycHugujQg9k2wbmxjcpdYZyVLfV9WerTnafJ',
        'serumBids': '14ivtgssEBoBjuZJtSAPKYgpUK7DmnSwuPMqJoVTSgKJ',
        'serumMarket': '9wFFyRfZBsuAha4YcuxcXLKwMxJR43S7fPfQLusDBzvT',
        'ammAuthority': '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1',
        'ammOpenOrders': 'HRk9CMrpq7Jn9sh7mzxE8CChHG8dneX9p475QKz4Fsfc',
        'ammQuantities': '11111111111111111111111111111111',
        'serumProgramId': '9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin',
        'ammTargetOrders': 'CZza3Ej4Mc58MnxWA385itCC9jCo3L1D7zc3LKy1bZMR',
        'serumEventQueue': '5KKsLVU6TcbVDK4BS6K1DGDxnh4Q9xjYJ8XaDCG5t8ht',
        'serumVaultSigner': 'F8Vyqk3unwxkXukZFQeYyGmFfTG3CAX4v24iyrjEYBJV',
        'poolWithdrawQueue': 'G7xeGGLevkRwB5f44QNgQtrPKBdMfkT6ZZwpS9xcC97n',
        'poolPcTokenAccount': 'HLmqeL62xR1QoZ1HKKbXRrdN1p3phKpxRMb2VVopvBBz',
        'serumPcVaultAccount': '8CFo8bL8mZQK8abbFyypFMwEDd8tVJjHTTojMLgQTUSZ',
        'poolCoinTokenAccount': 'DQyrAcCrDXQ7NeoqGgDCZwBvWDcYmFCjSb9JtteuvPpz',
        'serumCoinVaultAccount':
            '36c6YqAwyGKQG66XEp2dJc5JqjaBNv7sVghEtJv4c7u6',
        'poolTempLpTokenAccount':
            'Awpt6N7ZYPBa4vG4BQNFhFxDj4sxExAA9rpBAoBw2uok',
    },
    '6UmmUiYoBjSrhakAobJw8BvkmJtDVxaeBtbt7rxWo1mg': {  # RAY-USDC
        'serumAsks': 'DC1HsWWRCXVg3wk2NndS5LTbce3axwUwUZH1RgnV4oDN',
        'serumBids': 'Hf84mYadE1VqSvVWAvCWc9wqLXak4RwXiPb4A91EAUn5',
        'serumMarket': '2xiv8A5xrJ7RnGdxXB42uFEkYHJjszEhaJyKKt4WaLep',
        'ammAuthority': '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1',
        'ammOpenOrders': 'J8u8nTHYtvudyqwLrXZboziN95LpaHFHpd97Jm5vtbkW',
        'ammQuantities': '11111111111111111111111111111111',
        'serumProgramId': '9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin',
        'ammTargetOrders': '3cji8XW5uhtsA757vELVFAeJpskyHwbnTSceMFY5GjVT',
        'serumEventQueue': 'H9dZt8kvz1Fe5FyRisb77KcYTaN8LEbuVAfJSnAaEABz',
        'serumVaultSigner': 'FmhXe9uG6zun49p222xt3nG1rBAkWvzVz7dxERQ6ouGw',
        'poolWithdrawQueue': 'ERiPLHrxvjsoMuaWDWSTLdCMzRkQSo8SkLBLYEmSokyr',
        'poolPcTokenAccount': 'Eqrhxd7bDUCH3MepKmdVkgwazXRzY6iHhEoBpY7yAohk',
        'serumPcVaultAccount': '22jHt5WmosAykp3LPGSAKgY45p7VGh4DFWSwp21SWBVe',
        'poolCoinTokenAccount': 'FdmKUE4UMiJYFK5ogCngHzShuVKrFXBamPWcewDr31th',
        'serumCoinVaultAccount':
            'GGcdamvNDYFhAXr93DWyJ8QmwawUHLCyRqWL3KngtLRa',
        'poolTempLpTokenAccount':
            'D1V5GMf3N26owUFcbz2qR5N4G81qPKQvS2Vc4SM73XGB',
    },
}

# Struct for decoding data from Raydium Pool API
AMM_INFO_LAYOUT = CStruct(
    'status' / U64,
    'nonce' / U64,
    'orderNum' / U64,
    'depth' / U64,
    'coinDecimals' / U64,
    'pcDecimals' / U64,
    'state' / U64,
    'resetFlag' / U64,
    'minSize' / U64,
    'volMaxCutRatio' / U64,
    'amountWaveRatio' / U64,
    'coinLotSize' / U64,
    'pcLotSize' / U64,
    'minPriceMultiplier' / U64,
    'maxPriceMultiplier' / U64,
    'systemDecimalsValue' / U64,
    'minSeparateNumerator' / U64,
    'minSeparateDenominator' / U64,
    'tradeFeeNumerator' / U64,
    'tradeFeeDenominator' / U64,
    'pnlNumerator' / U64,
    'pnlDenominator' / U64,
    'swapFeeNumerator' / U64,
    'swapFeeDenominator' / U64,
    'needTakePnlCoin' / U64,
    'needTakePnlPc' / U64,
    'totalPnlPc' / U64,
    'totalPnlCoin' / U64,
    'poolTotalDepositPc' / U128,
    'poolTotalDepositCoin' / U128,
    'swapCoinInAmount' / U128,
    'swapPcOutAmount' / U128,
    'swapCoin2PcFee' / U64,
    'swapPcInAmount' / U128,
    'swapCoinOutAmount' / U128,
    'swapPc2CoinFee' / U64,
    'poolCoinTokenAccount' / U8[32],
    'poolPcTokenAccount' / U8[32],
    'coinMintAddress' / U8[32],
    'pcMintAddress' / U8[32],
    'lpMintAddress' / U8[32],
    'ammOpenOrders' / U8[32],
    'serumMarket' / U8[32],
    'serumProgramId' / U8[32],
    'ammTargetOrders' / U8[32],
    'poolWithdrawQueue' / U8[32],
    'poolTempLpTokenAccount' / U8[32],
    'ammOwner' / U8[32],
    'pnlOwner' / U8[32],
)


def convert_container(container):
    """
    Converts every container's attribute from bytearray to base58 string
    """

    for key, value in container.items():
        if isinstance(value, ListContainer):
            setattr(container, key, bytearray_to_base58(value))

    return container


def get_all_raydium_pools() -> dict:
    """
    Returns dict of best existing pools for Raydium swaps
    """

    response = send_get_request(RAYDIUM_POOL_API_URL)
    pool_dict = dict()

    if not response:
        raise TradeError('Request to RAYDIUM pool API returned empty.')

    for data in response.get('result'):
        decoded_data = base64_decode(data.get('account').get('data')[0])
        pool = convert_container(
            container=AMM_INFO_LAYOUT.parse(
                decoded_data,
            )
        )
        pool.ammId = data.get('pubkey')
        pool_name = f'{pool.pcMintAddress}-{pool.coinMintAddress}'

        if (
            pool.swapPcInAmount
            > pool_dict.get(pool_name, {}).get('swapPcInAmount', 0)
        ):
            pool_dict.update(
                {
                    f'{pool.pcMintAddress}-{pool.coinMintAddress}': pool
                }
            )

    return pool_dict


def get_pool_info(first_token_address, second_token_address):
    """
    Returns best pool for pair of tokens
    """

    if second_token_address == SOLANA_NATIVE_TOKEN_ADDRESS:
        second_token_address = SOLANA_WRAPPED_TOKEN_ADDRESS

    pools_dict = get_all_raydium_pools()
    pool = pools_dict.get(f'{first_token_address}-{second_token_address}')

    if not pool:
        pool = pools_dict.get(f'{second_token_address}-{first_token_address}')

    return pool


# def get_transaction_addresses(tx_hash: str):
#     from trades.models import TradeParams
#
#     trade_params = TradeParams.displayed_objects.filter(
#         from_tx_hash__iexact=tx_hash,
#     ).first()
#
#     return trade_params.json_data['pool']


def get_relayer_keypair() -> Keypair:
    """
    Get relayer keys for signing transaction in Solana network
    """

    with open(settings.JSON_ENV_FILE, 'r') as json_file:
        json_data = json_loads(json_file.read())

    keypair_relayer = Keypair(
        keypair=json_data.get('SOLANA_RELAYER_PRIVATE_KEY', [])[:32]
    )

    return keypair_relayer


def create_token_account(
    owner: PublicKey,
    mint: PublicKey,
    http_client: Client
) -> PublicKey:
    """
    Creates token account for user's wallet.
    It's necessary for successful transaction.
    """

    token_client = Token(
        conn=http_client,
        pubkey=mint,
        program_id=TOKEN_PROGRAM_ID,
        payer=get_relayer_keypair(),
    )
    token_account_address = token_client \
        .create_associated_token_account(owner=owner,)
    wait_count = 6
    wait_seconds = 5

    while not http_client.get_account_info(
            pubkey=token_account_address,
    ).get('result', {}).get('value') and wait_count > 0:
        sleep(wait_seconds)

    return token_account_address


def get_token_account_address(
    owner: PublicKey,
    mint: PublicKey,
    http_client: Client,
) -> PublicKey:
    """
    Returns token account for user's wallet.
    Creates it if it's not already exist.
    It's necessary for successful transaction.
    """

    token_account_address = get_associated_token_address(
        owner=owner,
        mint=mint,
    )

    if (
        not http_client.get_account_info(
            pubkey=token_account_address,
        )
        .get('result', {})
        .get('value')
    ):
        token_account_address = create_token_account(
            owner=owner,
            mint=mint,
            http_client=http_client,
        )

    return token_account_address


# PARAMS FIND ADDRESS FUNCS
def get_config_id(program_id: PublicKey, version: int, version_struct):
    return PublicKey.find_program_address(
        seeds=[
            bytes(PREFIX.encode('utf-8')),
            bytes(CONFIG.encode('utf-8')),
            version_struct.build({'version': version})
        ],
        program_id=program_id
    )[0]


def get_pda_confidant_id(program_id: PublicKey, confidant_id, confidant: str):
    return PublicKey.find_program_address(
        seeds=[
            bytes(PREFIX.encode('utf-8')),
            bytes(confidant.encode('utf-8')),
            confidant_id,
        ],
        program_id=program_id
    )[0]


def get_pda_transaction_id(program_id: PublicKey, original_tx_hash):
    return PublicKey.find_program_address(
        seeds=[
            bytes(PREFIX.encode('utf-8')),
            bytes(TRANSACTION.encode('utf-8')),
            original_tx_hash,
        ],
        program_id=program_id
    )[0]


def build_and_send_transaction_solana(
    wallet_address: str,
    rbc_amount_in: int,
    amount_out_min: int,
    original_tx_hash: str,
    signature: str,
    network: Network,
    receive_token_address: str,
):
    try:
        solana_client = Client(network.rpc_url_list[0])

        # Config structs
        # prefix_struct = CStruct('prefix' / U8[6])
        # config_struct = CStruct('config' / String)
        version_struct = CStruct('version' / U64)

        # PDA relayer structs
        # relayer_struct = CStruct('relayer' / String)
        # confidant_struct = CStruct('confidant' / U8[32])

        # INSTRUCTION STRUCTS
        instruction = CStruct(
            'instruction_number' / U8,
            'user' / U8[32],
            'amount_with_fee' / U64,
            'amount_out_min' / U64,
            'original_tx_hash' / U8[32],
            'validator_sign' / U8[65],
            'is_refund' / Bool,
            'transfer_data_type' / U8,
        )

        wallet_address_bytes = bytes_to_bytearray(
            byte_string=bytes(PublicKey(wallet_address)),
        )
        original_tx_hash_bytes = bytes_to_bytearray(
            byte_string=Web3.toBytes(hexstr=original_tx_hash)
        )
        validator_sign = bytes_to_bytearray(
            byte_string=Web3.toBytes(hexstr=signature)
        )

        # GET ACCOUNT PARAMS
        config_id = get_config_id(
            program_id=PROGRAM_ID,
            version=VERSION,
            version_struct=version_struct,
        )

        # 4xUq6Ndzm3EKQDMdVeFHd8Rt5ZzN4swLUWYES9dB96cR - CONFIG
        pda_relayer_id = get_pda_confidant_id(
            program_id=PROGRAM_ID,
            confidant_id=bytes(RELAYER_PUBLIC_KEY),
            confidant='relayer',
        )

        # pda_validator_id = get_pda_confidant_id(
        #     program_id=PROGRAM_ID,
        #     confidant_id=bytes(VALIDATOR_PUBLIC_KEY),
        #     confidant='validator',
        # )

        pda_transaction_id = get_pda_transaction_id(
            program_id=PROGRAM_ID,
            original_tx_hash=bytes(original_tx_hash_bytes),
        )

        keys = [
            # Config
            AccountMeta(pubkey=config_id, is_signer=False, is_writable=False),
            AccountMeta(
                pubkey=RELAYER_PUBLIC_KEY,
                is_signer=True,
                is_writable=False,
            ),
            AccountMeta(
                pubkey=pda_relayer_id,
                is_signer=False,
                is_writable=False,
            ),
            # AccountMeta(VALIDATOR_PUBLIC_KEY, False, False),
            # AccountMeta(pda_validator_id, False, False),
            AccountMeta(
                pubkey=pda_transaction_id,
                is_signer=False,
                is_writable=True,
            ),
            AccountMeta(
                pubkey=SYS_PROGRAM_ID,
                is_signer=False,
                is_writable=False,
            ),
            # USER
            # pda pool
            AccountMeta(
                pubkey=PublicKey(
                    '6rvuMQ7B3cwpmPHhbMGQFBsfDfkgnxiwmWxxSnkd9FjK'),
                is_signer=False,
                is_writable=True,
            ),
            AccountMeta(
                pubkey=PublicKey(
                    'DrmQS74dx5yDPzAJdGpVMqpSkVP9RXFQnMQAdeo1P7mj'),
                is_signer=False,
                is_writable=True,
            ),
        ]

        transfer_data_type = TRANSFER_DATA_TYPE.get(receive_token_address, 0)

        if transfer_data_type == NOT_TRANSFER_TOKEN_TYPE:
            pool_info = get_pool_info(
                first_token_address=SOLANA_TRANSFER_TOKEN_ADDRESS,
                second_token_address=receive_token_address,
            )

            serum_pool_info = SERUM_POOLS.get(pool_info.get('ammId'), {})

            keys.extend(
                [
                    AccountMeta(
                        pubkey=get_token_account_address(
                            owner=PublicKey(wallet_address),
                            mint=PublicKey(receive_token_address),
                            http_client=solana_client,
                        ),
                        is_signer=False,
                        is_writable=True,
                    ),
                    # SPL TOKEN
                    AccountMeta(
                        pubkey=TOKEN_PROGRAM_ID,
                        is_signer=False,
                        is_writable=False,
                    ),
                    # AMM
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('ammId')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(AMM_AUTHORITY),
                        is_signer=False,
                        is_writable=False,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('ammOpenOrders')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('ammTargetOrders')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get(
                            'poolCoinTokenAccount')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('poolPcTokenAccount')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(SERUM_PROGRAM_ID_V3),
                        is_signer=False,
                        is_writable=False,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('serumMarket')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(serum_pool_info.get('serumBids')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(serum_pool_info.get('serumAsks')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(
                            serum_pool_info.get('serumEventQueue')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(
                            serum_pool_info.get('serumCoinVaultAccount')
                        ),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(
                            serum_pool_info.get('serumPcVaultAccount')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(
                            serum_pool_info.get('serumVaultSigner')),
                        is_signer=False,
                        is_writable=False,
                    ),
                    # RADIUM
                    AccountMeta(
                        pubkey=PublicKey(LIQUIDITY_POOL_PROGRAM_ID_V4),
                        is_signer=False,
                        is_writable=False,
                    ),
                ]
            )
        elif transfer_data_type == TRANSFER_TOKEN_TYPE:
            keys.extend(
                [
                    AccountMeta(
                        pubkey=get_token_account_address(
                            owner=PublicKey(wallet_address),
                            mint=PublicKey(receive_token_address),
                            http_client=solana_client,
                        ),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=TOKEN_PROGRAM_ID,
                        is_signer=False,
                        is_writable=False,
                    ),
                ]
            )
        elif transfer_data_type == NATIVE_TOKEN_TYPE:
            pool_info = get_pool_info(
                first_token_address=SOLANA_TRANSFER_TOKEN_ADDRESS,
                second_token_address=receive_token_address,
            )
            serum_pool_info = SERUM_POOLS.get(pool_info.get('ammId'), {})

            keys.extend(
                [
                    AccountMeta(
                        pubkey=PublicKey(SOLANA_WRAPPED_TOKEN_ADDRESS),
                        is_signer=False,
                        is_writable=False,
                    ),
                    AccountMeta(
                        pubkey=PDA_WRAPPED,
                        is_signer=False,
                        is_writable=True,
                    ),
                    # SPL TOKEN
                    AccountMeta(
                        pubkey=TOKEN_PROGRAM_ID,
                        is_signer=False,
                        is_writable=False,
                    ),
                    # SPL TOKEN
                    AccountMeta(
                        pubkey=TOKEN_PROGRAM_ID,
                        is_signer=False,
                        is_writable=False,
                    ),
                    # AMM
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('ammId')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(AMM_AUTHORITY),
                        is_signer=False,
                        is_writable=False,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('ammOpenOrders')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('ammTargetOrders')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get(
                            'poolCoinTokenAccount')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('poolPcTokenAccount')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(SERUM_PROGRAM_ID_V3),
                        is_signer=False,
                        is_writable=False,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(pool_info.get('serumMarket')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(serum_pool_info.get('serumBids')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(serum_pool_info.get('serumAsks')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(
                            serum_pool_info.get('serumEventQueue')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(serum_pool_info.get(
                            'serumCoinVaultAccount')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(serum_pool_info.get(
                            'serumPcVaultAccount')),
                        is_signer=False,
                        is_writable=True,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(
                            serum_pool_info.get('serumVaultSigner')),
                        is_signer=False,
                        is_writable=False,
                    ),
                    # RAYDIUM
                    AccountMeta(
                        pubkey=PublicKey(LIQUIDITY_POOL_PROGRAM_ID_V4),
                        is_signer=False,
                        is_writable=False,
                    ),
                    AccountMeta(
                        pubkey=PublicKey(wallet_address),
                        is_signer=False,
                        is_writable=True,
                    ),
                ]
            )

        instruction_bytes = instruction.build(
            {
                'instruction_number': INSTRUCTION_NUMBER,
                'user': wallet_address_bytes,
                'amount_with_fee': rbc_amount_in,
                'amount_out_min': amount_out_min,
                'original_tx_hash': original_tx_hash_bytes,
                'validator_sign': validator_sign,
                'is_refund': False,
                'transfer_data_type': transfer_data_type,
            }
        )
        recent_blockhash = solana_client.get_recent_blockhash()
        recent_blockhash = Blockhash(
            recent_blockhash.get('result').get('value').get('blockhash')
        )
        transaction = Transaction(
            recent_blockhash=recent_blockhash,
            fee_payer=RELAYER_PUBLIC_KEY
        ) \
            .add(
                TransactionInstruction(
                    keys,
                    PROGRAM_ID,
                    instruction_bytes
                )
        )
        relayer_keypair = get_relayer_keypair()
        transaction.add_signer(signer=relayer_keypair)

        for key in keys:
            info(key)

        while 1:
            try:
                result = solana_client.send_transaction(
                    transaction,
                    relayer_keypair,
                    # opts=SolanaTxnOpts(
                    #     skip_confirmation=False,
                    # )
                )

                solana_client.confirm_transaction(
                    tx_sig=result.get('result'),
                    # commitment=Confirmed,
                    sleep_seconds=10,
                )

                return result.get('result')
            except (
                SolanaUnconfirmedTxError,
            ) as exception_error:
                exception(TRANSACTION_ERROR.format(exception_error))

                continue
    except RequestsConnectionError as exception_error:
        exception(REQUEST_ERROR.format(exception_error))

        return build_and_send_transaction_solana(
            wallet_address=wallet_address,
            rbc_amount_in=rbc_amount_in,
            amount_out_min=amount_out_min,
            original_tx_hash=original_tx_hash,
            signature=signature,
            network=network,
            receive_token_address=receive_token_address,
        )
