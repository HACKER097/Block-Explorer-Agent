import json
from typing import Dict, Any
from web3 import Web3
from fastmcp import FastMCP


RPC_URL = "https://eth.llamarpc.com"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

mcp = FastMCP("blockchain-mcp")

@mcp.tool
def transaction_to_details(tx_hash: str) -> Dict:
    tx = w3.eth.get_transaction(tx_hash)
    return Web3.to_json(tx)

if __name__ == "__main__":
    mcp.run()
