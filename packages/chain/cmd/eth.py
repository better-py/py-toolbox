import json
import os
import shutil
from typing import Optional, Callable

import click
import web3
from web3 import Web3


class ETHScaner(object):
    """

    """

    def __init__(self, rpc_url: str):
        print(f"init eth, rpc url: {rpc_url}")
        self.client = web3.Web3(Web3.HTTPProvider(rpc_url))

    def scan(self, address: str, tx_type: str, tx_count: int, ):
        print("scan eth:", address, tx_type, tx_count)
        ok = self.client.isConnected()
        print("is connected:", ok)
        pass


@click.command()
@click.option("--rpc_url", default="", help="eth rpc url")
@click.option("--address", default="", help="eth address")
@click.option("--tx_type", default="", help="eth tx type")
@click.option("--tx_count", default=0, help="eth tx count")
def main(rpc_url: str, address: str, tx_type: str, tx_count: int):
    r = ETHScaner(rpc_url=rpc_url)
    r.scan(address=address, tx_type=tx_type, tx_count=tx_count)


if __name__ == '__main__':
    main()
