# flake8: noqa
from django.test import TestCase

from contracts.models import Contract

from crosschain_backend.consts import DEFAULT_CRYPTO_ADDRESS

from integrators.models import SDKIntegrator

from networks.models import Network

from trades.services.functions import _add_trade_signature

from validators.models import Validator


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI = [
            {
                'anonymous': False,
                'inputs': [
                    {
                        'indexed': False,
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address',
                    }
                ],
                'name': 'Paused',
                'type': 'event',
            },
            {
                'anonymous': False,
                'inputs': [
                    {
                        'indexed': True,
                        'internalType': 'bytes32',
                        'name': 'role',
                        'type': 'bytes32',
                    },
                    {
                        'indexed': True,
                        'internalType': 'bytes32',
                        'name': 'previousAdminRole',
                        'type': 'bytes32',
                    },
                    {
                        'indexed': True,
                        'internalType': 'bytes32',
                        'name': 'newAdminRole',
                        'type': 'bytes32',
                    }
                ],
                'name': 'RoleAdminChanged',
                'type': 'event',
            },
            {
                'anonymous': False,
                'inputs': [
                    {
                        'indexed': True,
                        'internalType': 'bytes32',
                        'name': 'role',
                        'type': 'bytes32',
                    },
                    {
                        'indexed': True,
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address',
                    },
                    {
                        'indexed': True,
                        'internalType': 'address',
                        'name': 'sender',
                        'type': 'address',
                    }
                ],
                'name': 'RoleGranted',
                'type': 'event',
            },
            {
                'anonymous': False,
                'inputs': [
                    {
                        'indexed': True,
                        'internalType': 'bytes32',
                        'name': 'role',
                        'type': 'bytes32'
                    },
                    {
                        'indexed': True,
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address'
                    },
                    {
                        'indexed': True,
                        'internalType': 'address',
                        'name': 'sender',
                        'type': 'address'
                    }
                ],
                'name': 'RoleRevoked',
                'type': 'event'
            },
            {
                'anonymous': False,
                'inputs': [
                    {
                        'indexed': False,
                        'internalType': 'uint256',
                        'name': 'RBCAmountIn',
                        'type': 'uint256'
                    },
                    {
                        'indexed': False,
                        'internalType': 'uint256',
                        'name': 'amountSpent',
                        'type': 'uint256'
                    },
                    {
                        'indexed': False,
                        'internalType': 'address',
                        'name': 'provider',
                        'type': 'address'
                    }
                ],
                'name': 'TransferCryptoToOtherBlockchainUser',
                'type': 'event'
            },
            {
                'anonymous': False,
                'inputs': [
                    {
                        'indexed': False,
                        'internalType': 'address',
                        'name': 'user',
                        'type': 'address'
                    },
                    {
                        'indexed': False,
                        'internalType': 'uint256',
                        'name': 'amount',
                        'type': 'uint256'
                    },
                    {
                        'indexed': False,
                        'internalType': 'uint256',
                        'name': 'amountWithoutFee',
                        'type': 'uint256'
                    },
                    {
                        'indexed': False,
                        'internalType': 'bytes32',
                        'name': 'originalTxHash',
                        'type': 'bytes32'
                    }
                ],
                'name': 'TransferFromOtherBlockchain',
                'type': 'event'
            },
            {
                'anonymous': False,
                'inputs': [
                    {
                        'indexed': False,
                        'internalType': 'uint256',
                        'name': 'RBCAmountIn',
                        'type': 'uint256'
                    },
                    {
                        'indexed': False,
                        'internalType': 'uint256',
                        'name': 'amountSpent',
                        'type': 'uint256'
                    },
                    {
                        'indexed': False,
                        'internalType': 'address',
                        'name': 'provider',
                        'type': 'address'
                    }
                ],
                'name': 'TransferTokensToOtherBlockchainUser',
                'type': 'event'
            },
            {
                'anonymous': False,
                'inputs': [
                    {
                        'indexed': False,
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address'
                    }
                ],
                'name': 'Unpaused',
                'type': 'event'
            },
            {
                'inputs': [],
                'name': 'DEFAULT_ADMIN_ROLE',
                'outputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                                'type': 'bytes32'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'MANAGER_ROLE',
                'outputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                                'type': 'bytes32'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'OWNER_ROLE',
                'outputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                                'type': 'bytes32'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'RELAYER_ROLE',
                'outputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                                'type': 'bytes32'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                        'type': 'uint256'
                    }
                ],
                'name': 'RubicAddresses',
                'outputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                                'type': 'bytes32'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'SIGNATURE_LENGTH',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'VALIDATOR_ROLE',
                'outputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                                'type': 'bytes32'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'accTokenFee',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                        'type': 'uint256'
                    }
                ],
                'name': 'blockchainCryptoFee',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'blockchainRouter',
                'outputs': [
                    {
                        'internalType': 'address',
                        'name': '',
                                'type': 'address'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'bytes32',
                        'name': 'hash',
                        'type': 'bytes32'
                    },
                    {
                        'internalType': 'bytes',
                        'name': 'signature',
                        'type': 'bytes'
                    },
                    {
                        'internalType': 'uint256',
                        'name': 'offset',
                        'type': 'uint256'
                    }
                ],
                'name': 'ecOffsetRecover',
                'outputs': [
                    {
                        'internalType': 'address',
                        'name': '',
                                'type': 'address'
                    }
                ],
                'stateMutability': 'pure',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                        'type': 'uint256'
                    }
                ],
                'name': 'existingOtherBlockchain',
                'outputs': [
                    {
                        'internalType': 'bool',
                        'name': '',
                                'type': 'bool'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                        'type': 'uint256'
                    }
                ],
                'name': 'feeAmountOfBlockchain',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'address',
                        'name': 'user',
                        'type': 'address'
                    },
                    {
                        'internalType': 'uint256',
                        'name': 'amountWithFee',
                        'type': 'uint256'
                    },
                    {
                        'internalType': 'bytes32',
                        'name': 'originalTxHash',
                        'type': 'bytes32'
                    },
                    {
                        'internalType': 'uint256',
                        'name': 'blockchainNum',
                        'type': 'uint256'
                    }
                ],
                'name': 'getHashPacked',
                'outputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                                'type': 'bytes32'
                    }
                ],
                'stateMutability': 'pure',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'bytes32',
                        'name': 'role',
                        'type': 'bytes32'
                    }
                ],
                'name': 'getRoleAdmin',
                'outputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                                'type': 'bytes32'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'bytes32',
                        'name': 'role',
                        'type': 'bytes32'
                    },
                    {
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address'
                    }
                ],
                'name': 'grantRole',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'internalType': 'bytes32',
                        'name': 'role',
                        'type': 'bytes32'
                    },
                    {
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address'
                    }
                ],
                'name': 'hasRole',
                'outputs': [
                    {
                        'internalType': 'bool',
                        'name': '',
                                'type': 'bool'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address'
                    }
                ],
                'name': 'isRelayer',
                'outputs': [
                    {
                        'internalType': 'bool',
                        'name': '',
                                'type': 'bool'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address'
                    }
                ],
                'name': 'isValidator',
                'outputs': [
                    {
                        'internalType': 'bool',
                        'name': '',
                                'type': 'bool'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'maxGasPrice',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'maxTokenAmount',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'minConfirmationBlocks',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'minConfirmationSignatures',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'minTokenAmount',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'numOfThisBlockchain',
                'outputs': [
                    {
                        'internalType': 'uint128',
                        'name': '',
                                'type': 'uint128'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [],
                'name': 'paused',
                'outputs': [
                    {
                        'internalType': 'bool',
                        'name': '',
                                'type': 'bool'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                        'type': 'bytes32'
                    }
                ],
                'name': 'processedTransactions',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'bytes32',
                        'name': 'role',
                        'type': 'bytes32'
                    },
                    {
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address'
                    }
                ],
                'name': 'renounceRole',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'internalType': 'bytes32',
                        'name': 'role',
                        'type': 'bytes32'
                    },
                    {
                        'internalType': 'address',
                        'name': 'account',
                        'type': 'address'
                    }
                ],
                'name': 'revokeRole',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'internalType': 'bytes4',
                        'name': 'interfaceId',
                        'type': 'bytes4'
                    }
                ],
                'name': 'supportsInterface',
                'outputs': [
                    {
                        'internalType': 'bool',
                        'name': '',
                                'type': 'bool'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'bytes32',
                        'name': 'hash',
                        'type': 'bytes32'
                    }
                ],
                'name': 'toEthSignedMessageHash',
                'outputs': [
                    {
                        'internalType': 'bytes32',
                        'name': '',
                                'type': 'bytes32'
                    }
                ],
                'stateMutability': 'pure',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToOtherBlockchain',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function',
                'payable': True
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToOtherBlockchain',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function',
                'payable': True
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToUserWithFee',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToUserWithFee',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToOtherBlockchain1',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToOtherBlockchain1',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToUserWithFee1',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToUserWithFee1',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToOtherBlockchain2',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToOtherBlockchain2',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToUserWithFee2',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToUserWithFee2',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'firstPath',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContractV3.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToOtherBlockchainV3',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'firstPath',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContractV3.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToOtherBlockchainV3',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'path',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContractV3.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToUserWithFeeV3',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'path',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContractV3.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToUserWithFeeV3',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToOtherBlockchainAVAX',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToOtherBlockchainAVAX',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToUserWithFeeAVAX',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToUserWithFeeAVAX',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToOtherBlockchainAVAX1',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'firstPath',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'withFee',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToOtherBlockchainAVAX1',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToUserWithFeeAVAX1',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address[]',
                                'name': 'path',
                                'type': 'address[]'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContract.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToUserWithFeeAVAX1',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'firstPath',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContractV3.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToOtherBlockchainALGB',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenInAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'firstPath',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'exactRBCtokenOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapExactFor',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContractV3.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToOtherBlockchainALGB',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'path',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContractV3.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToUserWithFeeALGB',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'path',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContractV3.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToUserWithFeeALGB',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'srcAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address',
                                'name': 'srcToken',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'minTransitOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'data',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContractInch.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToOtherBlockchainInch',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function',
                'payable': True
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'uint256',
                                'name': 'blockchain',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'srcAmount',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'address',
                                'name': 'srcToken',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bytes32[]',
                                'name': 'secondPath',
                                'type': 'bytes32[]'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'minTransitOut',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'tokenOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'newAddress',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'bool',
                                'name': 'swapToCrypto',
                                'type': 'bool'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'data',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'string',
                                'name': 'signature',
                                'type': 'string'
                            }
                        ],
                        'internalType': 'struct ISwapContractInch.swapToParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToOtherBlockchainInch',
                'outputs': [],
                'stateMutability': 'payable',
                'type': 'function',
                'payable': True
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'dstToken',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'data',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContractInch.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapTokensToUserWithFeeInch',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'components': [
                            {
                                'internalType': 'address',
                                'name': 'user',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'provider',
                                'type': 'address'
                            },
                            {
                                'internalType': 'address',
                                'name': 'dstToken',
                                'type': 'address'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'initBlockchainNum',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountWithFee',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'uint256',
                                'name': 'amountOutMin',
                                'type': 'uint256'
                            },
                            {
                                'internalType': 'bytes32',
                                'name': 'originalTxHash',
                                'type': 'bytes32'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'concatSignatures',
                                'type': 'bytes'
                            },
                            {
                                'internalType': 'bytes',
                                'name': 'data',
                                'type': 'bytes'
                            }
                        ],
                        'internalType': 'struct ISwapContractInch.swapFromParams',
                        'name': 'params',
                        'type': 'tuple'
                    }
                ],
                'name': 'swapCryptoToUserWithFeeInch',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'internalType': 'uint128',
                        'name': '_blockchainNum',
                        'type': 'uint128'
                    },
                    {
                        'internalType': 'uint256',
                        'name': 'feeAmount',
                        'type': 'uint256'
                    }
                ],
                'name': 'setCryptoFeeOfBlockchain',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'internalType': 'address',
                        'name': '_provider',
                        'type': 'address'
                    }
                ],
                'name': 'getProviderFee',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'address',
                        'name': '_provider',
                        'type': 'address'
                    }
                ],
                'name': 'getAmountOfProvider',
                'outputs': [
                    {
                        'internalType': 'uint256',
                        'name': '',
                                'type': 'uint256'
                    }
                ],
                'stateMutability': 'view',
                'type': 'function',
                'constant': True
            },
            {
                'inputs': [
                    {
                        'internalType': 'address',
                        'name': '_provider',
                        'type': 'address'
                    },
                    {
                        'internalType': 'uint256',
                        'name': '_fee',
                        'type': 'uint256'
                    }
                ],
                'name': 'setProviderFee',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [],
                'name': 'collectProviderFee',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            },
            {
                'inputs': [
                    {
                        'internalType': 'address',
                        'name': '_provider',
                        'type': 'address'
                    }
                ],
                'name': 'collectProviderFee',
                'outputs': [],
                'stateMutability': 'nonpayable',
                'type': 'function'
            }
        ]
        RUBIC_MULTICHAIN_DEFAULT_TOKEN_CONTRACT_ABI = [
            {
                'name': 'name',
                'type': 'function',
                'inputs': [],
                'outputs': [
                    {
                        'name': '',
                        'type': 'string'
                    }
                ],
                'payable': False,
                'constant': True,
                'stateMutability': 'view'
            },
            {
                'name': 'approve',
                'type': 'function',
                'inputs': [
                    {
                        'name': '_spender',
                        'type': 'address'
                    },
                    {
                        'name': '_value',
                        'type': 'uint256'
                    }
                ],
                'outputs': [
                    {
                        'name': '',
                        'type': 'bool'
                    }
                ],
                'payable': False,
                'constant': False,
                'stateMutability': 'nonpayable'
            },
            {
                'name': 'totalSupply',
                'type': 'function',
                'inputs': [

                ],
                'outputs': [
                    {
                        'name': '',
                        'type': 'uint256'
                    }
                ],
                'payable': False,
                'constant': True,
                'stateMutability': 'view'
            },
            {
                'name': 'transferFrom',
                'type': 'function',
                'inputs': [
                    {
                        'name': '_from',
                        'type': 'address'
                    },
                    {
                        'name': '_to',
                        'type': 'address'
                    },
                    {
                        'name': '_value',
                        'type': 'uint256'
                    }
                ],
                'outputs': [
                    {
                        'name': '',
                        'type': 'bool'
                    }
                ],
                'payable': False,
                'constant': False,
                'stateMutability': 'nonpayable'
            },
            {
                'name': 'decimals',
                'type': 'function',
                'inputs': [

                ],
                'outputs': [
                    {
                        'name': '',
                        'type': 'uint8'
                    }
                ],
                'payable': False,
                'constant': True,
                'stateMutability': 'view'
            },
            {
                'name': 'balanceOf',
                'type': 'function',
                'inputs': [
                    {
                        'name': '_owner',
                        'type': 'address'
                    }
                ],
                'outputs': [
                    {
                        'name': 'balance',
                        'type': 'uint256'
                    }
                ],
                'payable': False,
                'constant': True,
                'stateMutability': 'view'
            },
            {
                'name': 'symbol',
                'type': 'function',
                'inputs': [

                ],
                'outputs': [
                    {
                        'name': '',
                        'type': 'string'
                    }
                ],
                'payable': False,
                'constant': True,
                'stateMutability': 'view'
            },
            {
                'name': 'transfer',
                'type': 'function',
                'inputs': [
                    {
                        'name': '_to',
                        'type': 'address'
                    },
                    {
                        'name': '_value',
                        'type': 'uint256'
                    }
                ],
                'outputs': [
                    {
                        'name': '',
                        'type': 'bool'
                    }
                ],
                'payable': False,
                'constant': False,
                'stateMutability': 'nonpayable'
            },
            {
                'name': 'allowance',
                'type': 'function',
                'inputs': [
                    {
                        'name': '_owner',
                        'type': 'address'
                    },
                    {
                        'name': '_spender',
                        'type': 'address'
                    }
                ],
                'outputs': [
                    {
                        'name': '',
                        'type': 'uint256'
                    }
                ],
                'payable': False,
                'constant': True,
                'stateMutability': 'view'
            },
            {
                'type': 'fallback',
                'payable': True,
                'stateMutability': 'payable'
            },
            {
                'name': 'Approval',
                'type': 'event',
                'inputs': [
                    {
                        'name': 'owner',
                        'type': 'address',
                        'indexed': True
                    },
                    {
                        'name': 'spender',
                        'type': 'address',
                        'indexed': True
                    },
                    {
                        'name': 'value',
                        'type': 'uint256',
                        'indexed': False
                    }
                ],
                'anonymous': False
            },
            {
                'name': 'Transfer',
                'type': 'event',
                'inputs': [
                    {
                        'name': 'from',
                        'type': 'address',
                        'indexed': True
                    },
                    {
                        'name': 'to',
                        'type': 'address',
                        'indexed': True
                    },
                    {
                        'name': 'value',
                        'type': 'uint256',
                        'indexed': False
                    }
                ],
                'anonymous': False
            }
        ]

        networks = {
            'solana': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'solana',
                    'type': 'solana',
                    'rpc_url_list': [
                        'https://api.mainnet-beta.solana.com',
                    ],
                    'explorer_url': 'https://solscan.io',
                },
            },
            'near': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'near',
                    'type': 'near',
                    'rpc_url_list': [
                        'https://rpc.mainnet.near.org',
                        'https://archival-rpc.mainnet.near.org',
                    ],
                    'explorer_url': 'https://explorer.near.org',
                },
            },
            'fantom': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'fantom',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        'https://rpc.ftm.tools',
                    ],
                    'explorer_url': 'https://ftmscan.com',
                },
            },
            'binance-smart-chain': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'binance-smart-chain',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        'https://bsc-dataseed.binance.org/',
                    ],
                    'explorer_url': 'https://bscscan.com',
                },
            },
            'avalanche': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'avalanche',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        'https://api.avax.network/ext/bc/C/rpc',
                    ],
                    'explorer_url': 'https://snowtrace.io',
                },
            },
            'telos-evm': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'telos-evm',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        'https://mainnet.telos.net/evm',
                    ],
                    'explorer_url': 'https://www.teloscan.io/',
                },
            },
            'polygon': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'polygon',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        'https://polygon-rpc.com',
                    ],
                    'explorer_url': 'https://polygonscan.com',
                },
            },
            'harmony': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'harmony',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        'https://api.harmony.one',
                        'https://s1.api.harmony.one',
                        'https://s2.api.harmony.one',
                        'https://s3.api.harmony.one',
                    ],
                    'explorer_url': 'https://explorer.harmony.one',
                },
            },
            'moonriver': {
                'model': 'networks.network',
                'pk': 'cec1920e-02cd-469b-a1e9-10fe1319281a',
                'fields': {
                    '_is_displayed': True,
                    'title': 'moonriver',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        'https://rpc.moonriver.moonbeam.network',
                    ],
                    'explorer_url': 'https://moonriver.moonscan.io',
                },
            },
            'aurora': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'aurora',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        'https://mainnet.aurora.dev',
                    ],
                    'explorer_url': 'https://aurorascan.dev',
                },
            },
            'arbitrum': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'arbitrum',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        'https://arb1.arbitrum.io/rpc',
                    ],
                    'explorer_url': 'https://explorer.arbitrum.io',
                },
            },
            'ethereum': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'ethereum',
                    'type': 'eth-like',
                    'rpc_url_list': [
                        (
                            'https://mainnet.infura.io/v3/'
                            '05bdb9eede9844d2bb4e770e9383c5b5'
                        ),
                    ],
                    'explorer_url': 'https://etherscan.io',
                },
            }
        }
        contracts = {
            'binance-smart-chain': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_BSC_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0x70e8C8139d1ceF162D5ba3B286380EB5913098c4',
                    'network': 'binance-smart-chain',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0x9902f3cf707ce064d17b4c2368c8f6b2551a70943f7c3429321842e9d2c55dcf'
                    ),
                    'percent_of_encreasing_gas_price': '1.20',
                    'min_gas_price': '5000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '74737563471371892',
                    'blockchain_number': 1,
                }
            },
            'ethereum': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_ETH_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0xD8b19613723215EF8CC80fC35A1428f8E8826940',
                    'network': 'ethereum',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0xcb99d1cc4ee13668087c2f8fcbe3c1f0b6a1e9bc682026fd03ffad5bda882843'
                    ),
                    'percent_of_encreasing_gas_price': '1.10',
                    'min_gas_price': '35000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '0',
                    'blockchain_number': 2,
                }
            },
            'polygon': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_POL_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0xeC52A30E4bFe2D6B0ba1D0dbf78f265c0a119286',
                    'network': 'polygon',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0x3a072246384a9c47a123203503a255ee1f7ecbbaefc3edabaeb3979e9662df91'
                    ),
                    'percent_of_encreasing_gas_price': '1.33',
                    'min_gas_price': '100000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '30196173761211068560',
                    'blockchain_number': 3,
                }
            },
            'avalanche': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_AVAX_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0x541eC7c03F330605a2176fCD9c255596a30C00dB',
                    'network': 'avalanche',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0x6190e909513d5f40ac78eb4aafe2adeeb71042b24e6f55f55a84ba8e43ad8967'
                    ),
                    'percent_of_encreasing_gas_price': '1.33',
                    'min_gas_price': '5000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '614196357249514436',
                    'blockchain_number': 4,
                }
            },
            'fantom': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_FTM_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0xd23B4dA264A756F427e13C72AB6cA5A6C95E4608',
                    'network': 'fantom',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0x69f2f46f5a1474f0f95b786ce1f4d5db980a04098b4b58ceb146cf90adfb829a'
                    ),
                    'percent_of_encreasing_gas_price': '1.50',
                    'min_gas_price': '5000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '56541485432262094214',
                    'blockchain_number': 5,
                }
            },
            'moonriver': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_MOVR_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0xD8b19613723215EF8CC80fC35A1428f8E8826940',
                    'network': 'moonriver',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0xb6eaa6a4f0bc0b785ed4a75623bf1519957c0d9f96c699514e0086fdcac53869'
                    ),
                    'percent_of_encreasing_gas_price': '1.33',
                    'min_gas_price': '5000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '443852356548639331',
                    'blockchain_number': 6,
                }
            },
            'harmony': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_HARMONY_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0x5681012ccc3ec5bafefac21ce4280ad7fe22bbf2',
                    'network': 'harmony',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0x8e3a5957876ab4d35c9f1bc111c36307acb856d78314325fe9b2394c1733f85b'
                    ),
                    'percent_of_encreasing_gas_price': '1.33',
                    'min_gas_price': '5000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '205825603195332638017',
                    'blockchain_number': 7,
                }
            },
            'solana': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'SOLANA_PROD',
                    'type': 'crosschain routing',
                    'address': 'r2TGRLHRtQ2Uj1CR7TCBYKgRxJi5M8FRjcqZnyQzYDB',
                    'network': 'solana',
                    'abi': {
                        'null': 'null'
                    },
                    'hash_of_creation': '0x0000000000000000000000000000000000000000',
                    'percent_of_encreasing_gas_price': '0.33',
                    'min_gas_price': '5000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '0',
                    'blockchain_number': 8,
                }
            },
            'near': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'NEAR_PROD',
                    'type': 'crosschain routing',
                    'address': 'multichain.rubic-finance.near',
                    'network': 'near',
                    'abi': {
                        'null': 'null'
                    },
                    'hash_of_creation': '',
                    'percent_of_encreasing_gas_price': '1.33',
                    'min_gas_price': '5000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '0',
                    'blockchain_number': 9,
                }
            },
            'arbitrum': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_ARBITRUM_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0x5f3c8d58a01aad4f875d55e2835d82e12f99723c',
                    'network': 'arbitrum',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0x2d4ffba38a162f9bc292543ca3c0612b7128526a4421a645e38b32c125fd01df'
                    ),
                    'percent_of_encreasing_gas_price': '1.33',
                    'min_gas_price': '5000000000',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '10354167102500000',
                    'blockchain_number': 10,
                }
            },
            'aurora': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_AURORA_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0x55be05ecc1c417b16163b000cb71dce8526a5d06',
                    'network': 'aurora',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0x8a476dc394069afebce8503ca1e6cd84dca9ba5e26484b5121267b5557aa9f9c'
                    ),
                    'percent_of_encreasing_gas_price': '1.33',
                    'min_gas_price': '0',
                    'default_average_volume_gas_used': '250000',
                    'current_gas_price': '14300938061455783',
                    'blockchain_number': 11,
                }
            },
            'telos-evm': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'RUBIC_SWAP_CONTRACT_IN_TELOS_EVM_PROD_READY',
                    'type': 'crosschain routing',
                    'address': '0x5356e4614864aa532071fe57bae20ed67e6f2e2c',
                    'network': 'telos-evm',
                    'abi': RUBIC_MULTICHAIN_DEFAULT_CONTRACT_ABI,
                    'hash_of_creation': (
                        '0xade0b7bf01118ab30f572444ef78256c63a8b3baabb9e5bd8344c7295a4d7c37'
                    ),
                    'percent_of_encreasing_gas_price': '1.20',
                    'min_gas_price': '5000000000',
                    'default_average_volume_gas_used': '150000',
                    'current_gas_price': '36935381717885171029',
                    'blockchain_number': 12,
                }
            },
        }
        validators = {
            'validator_2': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'VALIDATOR_2',
                    'type': 'main'
                }
            },
            'validator_sol_3': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'VALIDATOR_SOL_3',
                    'type': 'main'
                }
            },
            'validator_4': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'VALIDATOR_4',
                    'type': 'support'
                }
            },
            'validator_sol_2': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'VALIDATOR_SOL_2',
                    'type': 'main'
                }
            },
            'validator_sol_1': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'VALIDATOR_SOL_1',
                    'type': 'main'
                }
            },
            'validator_3': {
                'fields': {
                    '_created_at': '2021-11-30T13:06:38.166Z',
                    '_updated_at': '2021-11-30T13:06:38.166Z',
                    '_is_displayed': True,
                    'title': 'VALIDATOR_3',
                    'type': 'main'
                }
            },
            'validator_sol_4': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'VALIDATOR_SOL_4',
                    'type': 'support'
                }
            },
            'validator_1': {
                'fields': {
                    '_is_displayed': True,
                    'title': 'VALIDATOR_1',
                    'type': 'main'
                }
            }
        }
        integrators = {
            'default': {
                'fields': {
                    '_is_displayed': True,
                    'name': 'Default',
                    'wallet_address': DEFAULT_CRYPTO_ADDRESS,
                    'domain': '',
                    # 'platform_fee_percents': {},
                    # 'platform_fee_amounts_in_usd': {},
                }
            }
        }

        networks_to_create = [
            Network(
                title=network.get('fields').get('title'),
                type=network.get('fields').get('type'),
                rpc_url_list=network.get('fields').get('rpc_url_list'),
                explorer_url=network.get('fields').get('explorer_url'),
            )
            for network in networks.values()
        ]

        Network.objects.bulk_create(
            networks_to_create,
            ignore_conflicts=False,
        )

        crosschain_contracts_to_create = [
            Contract(
                title=contract.get('fields').get('title'),
                type=contract.get('fields').get('type'),
                address=contract.get('fields').get('address'),
                network=Network.displayed_objects.get(
                    title=contract.get('fields').get('network')
                ),
                abi=contract.get('fields').get('abi'),
                hash_of_creation=contract.get('fields')
                .get('hash_of_creation'),
                percent_of_encreasing_gas_price=contract.get('fields')
                .get('percent_of_encreasing_gas_price'),
                min_gas_price=contract.get('fields').get('min_gas_price'),
                default_average_volume_gas_used=contract.get('fields')
                .get('default_average_volume_gas_used'),
                current_gas_price=contract.get('fields')
                .get('current_gas_price'),
                blockchain_number=contract.get('fields')
                .get('blockchain_number'),
            )
            for contract in contracts.values()
        ]
        token_contracts_to_create = [
            Contract(
                title='ERC-20',
                type=Contract.TYPE_TOKEN,
                address=DEFAULT_CRYPTO_ADDRESS,
                network=network,
                abi=RUBIC_MULTICHAIN_DEFAULT_TOKEN_CONTRACT_ABI,
                percent_of_encreasing_gas_price=0,
                min_gas_price=0,
                default_average_volume_gas_used=0,
                current_gas_price=0,
                blockchain_number=0,
            )
            for network in Network.objects
            .filter(type=Network.TYPE_ETH_LIKE)
            .order_by('title')
            .distinct('title')
        ]

        # Create test crosschain contracts
        Contract.objects.bulk_create(
            crosschain_contracts_to_create,
            ignore_conflicts=False,
        )

        # Create test ERC-20 token contracts
        Contract.objects.bulk_create(
            token_contracts_to_create,
            ignore_conflicts=False,
        )

        validators_to_create = [
            Validator(
                title=validator.get('fields').get('title'),
                type=validator.get('fields').get('type'),
            )
            for validator in validators.values()
        ]

        Validator.objects.bulk_create(
            validators_to_create,
            ignore_conflicts=False,
        )

        integrators_to_create = [
            SDKIntegrator(
                name=integrator.get('fields').get('name'),
                wallet_address=integrator.get('fields').get('wallet_address'),
                domain=integrator.get('fields').get('domain'),
            )
            for integrator in integrators.values()
        ]

        SDKIntegrator.objects.bulk_create(
            integrators_to_create,
            ignore_conflicts=False,
        )


class ETHLikeTestCase(BaseTestCase):
    TEST_FROM_NETWORK_NUM = 3
    TEST_FROM_TXN_HASH = (
        '0x5308c3aad15b60452bf14b06509c3d1b'
        '45bfc1f39ce0628f655a6f9e34f15d04'
    )
    TEST_EVENT_NAME = 'TransferCryptoToOtherBlockchainUser'
    TEST_VALIDATOR_NAME = 'VALIDATOR_3'
    TEST_VALIDATOR_SIGNATURE = (
        '0924bc59b090e3783572c87844cadc3e'
        '25fd239e36832ff9f7b6586a3d88b432'
        '7d2f583a1b67c514d5f2fc6cf7432a02'
        '33439d1f3b491b0204110b48df374b3a1c'
    )

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        _add_trade_signature(
            from_contract_num=cls.TEST_FROM_NETWORK_NUM,
            from_tx_hash=cls.TEST_FROM_TXN_HASH,
            event_name=cls.TEST_EVENT_NAME,
            validator_name=cls.TEST_VALIDATOR_NAME,
            signature=cls.TEST_VALIDATOR_SIGNATURE,
        )
