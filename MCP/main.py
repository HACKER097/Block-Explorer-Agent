import json
from typing import Any, Union
from web3 import Web3
from fastmcp import FastMCP
import Decompiler
from Context import get_context, get_context_api

RPC_URL = "https://eth.llamarpc.com"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

mcp = FastMCP("blockchain-mcp")

@mcp.tool
def transaction_to_details(tx_hash: str) -> str:
    tx = w3.eth.get_transaction(tx_hash)
    return Web3.to_json(tx)

@mcp.tool
def block_to_transactions(block_number: str) -> str:
    block = w3.eth.get_block(int(block_number))
    return Web3.to_json(block)

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
