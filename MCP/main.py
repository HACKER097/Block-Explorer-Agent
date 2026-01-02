import json
from typing import Any, Union
from web3 import Web3
from fastmcp import FastMCP
import Decompiler
from Context import get_context, get_context_api
from browser_connect import get_active_etherscan_url

RPC_URL = "https://eth.llamarpc.com"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
mcp = FastMCP("blockchain-mcp")

ERC20_ABI = [
    {"constant": True, "inputs": [], "name": "name", "outputs": [{"type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"type": "uint256"}], "type": "function"},
]

@mcp.tool
def get_user_etherscan_tab_url() -> str:
    return str(get_active_etherscan_url())

@mcp.tool
def transaction_to_details(tx_hash: str) -> str:
    tx = w3.eth.get_transaction(tx_hash)
    return Web3.to_json(tx)

@mcp.tool
def get_latest_block_number() -> str:
    return str(w3.eth.block_number)


@mcp.tool
def block_to_transactions(block_number: str) -> str:
    block = w3.eth.get_block(int(block_number))
    return Web3.to_json(block)

@mcp.tool
def get_erc20_details(token_address: str) -> str:
    address = w3.to_checksum_address(token_address)
    contract = w3.eth.contract(address=address, abi=ERC20_ABI)
    
    details = {
        "address": address,
        "name": None,
        "symbol": None,
        "decimals": 18,  # Standard fallback
        "total_supply": 0
    }

    try:
        details["name"] = contract.functions.name().call()
    except Exception: pass

    try:
        details["symbol"] = contract.functions.symbol().call()
    except Exception: pass

    try:
        details["decimals"] = contract.functions.decimals().call()
    except Exception: pass

    try:
        raw_supply = contract.functions.totalSupply().call()
        details["total_supply"] = raw_supply / (10 ** details["decimals"])
    except Exception: pass

    return details

@mcp.tool
def address_to_transactions(address: str) -> str:
    # Need API
    return "Not implemented"

@mcp.tool
def get_transaction_trace(tx_hash: str) -> str:
    response = w3.provider.make_request("debug_traceTransaction", [ tx_hash, {"tracer": "callTracer"}])

    if 'result' in response:
        return response['result']
    elif 'error' in response:
        return response['error']

@mcp.tool
def get_contract_details(address: str) -> str:
    checksum_address = Web3.to_checksum_address(address)
    
    bytecode = w3.eth.get_code(checksum_address)
    
    is_contract = len(bytecode) > 0
    
    info = {
        "address": checksum_address,
        "is_contract": is_contract,
        "bytecode_size": len(bytecode),
        "balance_wei": w3.eth.get_balance(checksum_address),
        "transaction_count": w3.eth.get_transaction_count(checksum_address),
        "context": get_context_api(address)
    }
    
    return Web3.to_json(info)

@mcp.tool
def get_contract_code(address: str) -> str:
    checksum_address = Web3.to_checksum_address(address)
    bytecode = w3.eth.get_code(checksum_address)
    info = {"code": Decompiler.decompile(str(bytecode.hex()))}
    return Web3.to_json(info)

@mcp.tool
def get_address_details(address: str) -> str:
    checksum_address = Web3.to_checksum_address(address)
    
    info = {
        "address": checksum_address,
        "balance_wei": w3.eth.get_balance(checksum_address),
        "balance_eth": float(Web3.from_wei(w3.eth.get_balance(checksum_address), 'ether')),
        "nonce": w3.eth.get_transaction_count(checksum_address),
        "is_contract": len(w3.eth.get_code(checksum_address)) > 0,
        "context": get_context(checksum_address)
    }
    
    return Web3.to_json(info)

if __name__ == "__main__":
    mcp.run()
