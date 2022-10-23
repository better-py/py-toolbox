import json
import os
import shutil
from typing import Optional, Callable

import click
import web3
from web3 import Web3
from etherscan.accounts import Account


class ETHScaner(object):
    """
    reference:
        - etherscan.io api:
            - https://docs.etherscan.io/misc-tools-and-utilities/using-this-docs
            - https://github.com/corpetty/py-etherscan-api
            - https://github.com/pcko1/etherscan-python

    """

    def __init__(self, rpc_url: str, etherscan_api_key: str):
        print(f"init eth, rpc url: {rpc_url}")
        self.client = web3.Web3(Web3.HTTPProvider(rpc_url))
        if not self.client.isConnected():
            print(f"error: rpc not ok, invalid rpc url: {rpc_url}")

        self.etherscan_api_key = etherscan_api_key

    def balance(self, address: str):
        balance = self.client.eth.getBalance(address)
        eth_balance = self.client.fromWei(balance, "ether")

        print(f"address balance: {balance}, {eth_balance} ETH")

    def scan(self, address: str, tx_type: str, tx_count: int, ):
        print("scan eth:", address, tx_type, tx_count)

        transactions = self.client.eth.get_transaction_count(address)
        print(f"transactions: {transactions}, wait...")

        api = Account(address=address, api_key=self.etherscan_api_key)

        # txs = api.get_all_transactions(offset=10, sort='asc', internal=False)
        txs = api.get_transaction_page(offset=10, sort='desc', internal=False)

        for tx in txs:
            eth_balance = self.client.fromWei(int(tx['value']), "ether")
            print(f"\ttx: {tx['blockNumber']} {tx['hash']} {eth_balance}, {tx['from']} -> {tx['to']}")
            # print(f"\ttx:{tx}")


@click.command()
@click.option("--rpc_url", default="", help="eth rpc url")
@click.option("--etherscan_api_key", default="", help="etherscan api key")
@click.option("--address", default="", help="eth address")
@click.option("--tx_type", default="", help="eth tx type")
@click.option("--tx_count", default=0, help="eth tx count")
def main(rpc_url: str, etherscan_api_key: str, address: str, tx_type: str, tx_count: int, ):
    print(f"input args: {rpc_url}, {etherscan_api_key}, {address}, {tx_type}, {tx_count}")
    r = ETHScaner(rpc_url=rpc_url, etherscan_api_key=etherscan_api_key)
    r.balance(address)
    r.scan(address=address, tx_type=tx_type, tx_count=tx_count)


if __name__ == '__main__':
    main()
