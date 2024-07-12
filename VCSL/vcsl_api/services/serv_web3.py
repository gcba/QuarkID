from web3 import Web3
from kink import inject


@inject
class Web3Service:
    def __init__(self, url: str, wallet_priv_key: str, contract_addr: str, abi: str):
        self.web3 = Web3(Web3.HTTPProvider(url))
        self.account = self.web3.eth.account.from_key(wallet_priv_key)
        self.contract_addr = contract_addr
        if not self.web3.is_connected():
            raise Exception("Web3 is not connected")

        self.contract = self.web3.eth.contract(address=contract_addr, abi=abi)

    def set_issuer_url(self, new_issuer_url: str) -> bool:
        nonce = self.web3.eth.get_transaction_count(self.account.address)
        call_func = self.contract.functions.setUrl(new_issuer_url).build_transaction({
            'gas': 1000000,
            'gasPrice': self.web3.to_wei('40', 'gwei'),
            'from': self.account.address,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.sign_transaction(call_func, self.account._private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        _ = self.web3.eth.wait_for_transaction_receipt(txn_hash)
        return True  # TODO: Check if transaction was successful

    def add_vcsl(self, id: str, ipns: str) -> bool:
        nonce = self.web3.eth.get_transaction_count(self.account.address)
        call_func = self.contract.functions.addData(id, ipns).build_transaction({
            'gas': 1000000,
            'gasPrice': self.web3.to_wei('40', 'gwei'),
            'from': self.account.address,
            'nonce': nonce,
        })
        signed_txn = self.web3.eth.account.sign_transaction(call_func, self.account._private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        _ = self.web3.eth.wait_for_transaction_receipt(txn_hash)
        return True

    def get_issuer_url(self) -> str:
        return self.contract.functions.getUrl().call()

    def get_vcsl(self, id: str) -> str:
        return self.contract.functions.getData(id).call()
