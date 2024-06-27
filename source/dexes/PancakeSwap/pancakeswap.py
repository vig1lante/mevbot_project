from source.dexes.dex_class import DexClass
from web3.middleware import geth_poa_middleware


class PancakeSwapV3(DexClass):
    def __init__(self, provider_url):
        super().__init__(provider_url)
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def is_address(self, address):
        return self.web3.isAddress(address)

    def is_checksum_address(self, address):
        return self.web3.isChecksumAddress(address)

    def to_checksum_address(self, address):
        return self.web3.toChecksumAddress(address)

    def max_priority_fee(self):
        return self.web3.eth.max_priority_fee()

    def gas_price(self):
        return self.web3.eth.gasPrice

    def chain_id(self):
        return self.web3.eth.chain_id

    def get_balance(self, address):
        return self.web3.eth.get_balance(address)

    def get_block_number(self):
        return self.web3.eth.block_number

    def get_block(self, block_identifier):
        return self.web3.eth.get_block(block_identifier)

    def get_transaction(self, transaction_hash):
        return self.web3.eth.get_transaction(transaction_hash)

    def wait_for_transaction_receipt(self, transaction_hash, timeout=120):
        return self.web3.eth.wait_for_transaction_receipt(transaction_hash, timeout)

    def get_transaction_receipt(self, transaction_hash):
        return self.web3.eth.get_transaction_receipt(transaction_hash)

    def send_raw_transaction(self, signed_transaction):
        return self.web3.eth.send_raw_transaction(signed_transaction)

    def sign_transaction(self, transaction_dict, private_key):
        return self.web3.eth.account.sign_transaction(transaction_dict, private_key)

    def estimate_gas(self, transaction_dict):
        return self.web3.eth.estimate_gas(transaction_dict)

    def contract(self, address, abi):
        return self.web3.eth.contract(address=address, abi=abi)

    def get_pool_info(self, pool_address, pool_abi):
        contract = self.contract(pool_address, pool_abi)
        reserves = contract.functions.getReserves().call()
        return reserves

    def swap_tokens(self, router_address, router_abi, amount_in, amount_out_min, path, to, deadline, private_key):
        contract = self.contract(router_address, router_abi)
        transaction = contract.functions.swapExactTokensForTokens(
            amount_in,
            amount_out_min,
            path,
            to,
            deadline
        ).buildTransaction({
            'chainId': self.chain_id(),
            'gas': 2000000,
            'gasPrice': self.gas_price(),
            'nonce': self.web3.eth.get_transaction_count(to),
        })
        signed_tx = self.sign_transaction(transaction, private_key)
        tx_hash = self.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash
