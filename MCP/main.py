import json
from typing import Any, Union
from web3 import Web3
from fastmcp import FastMCP
from hexbytes import HexBytes
import requests

# We don't need these strictly for this specific fix, but keeping imports
import Decompiler
from Context import get_addr_context_api
from browser_connect import get_active_etherscan_url

RPC_URL = "https://eth.llamarpc.com"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
mcp = FastMCP("blockchain-mcp")

# ABI including transfer. 
# Note: decode_function_input only checks INPUTS, so the return type mismatch 
# for non-standard tokens like USDT (which return void instead of bool) won't break decoding.
ERC20_ABI = [
    {"constant": True, "inputs": [], "name": "name", "outputs": [{"type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"type": "uint256"}], "type": "function"},
    {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"},
]

@mcp.tool
def get_user_etherscan_tab_url() -> str:
    return str(get_active_etherscan_url())

@mcp.tool
def transaction_to_details(tx_hash: str) -> str:
    try:
        # 1. Fetch Transaction
        tx = w3.eth.get_transaction(tx_hash)
        
        # 2. Serialize to standard JSON string, then parse back to a mutable Dict
        # This solves all HexBytes serialization issues immediately.
        tx_data = json.loads(Web3.to_json(tx))
        
        # 3. Check for ERC20 'transfer' selector (0xa9059cbb)
        input_hex = tx_data.get('input', '')
        
        if input_hex.startswith('0xa9059cbb'):
            try:
                # Prepare contract for decoding (Address not strictly needed for decoding input)
                contract = w3.eth.contract(abi=ERC20_ABI)
                
                # CRITICAL: decode_function_input requires Bytes/HexBytes, NOT a string.
                decoded_func = contract.decode_function_input(HexBytes(input_hex))
                func_obj = decoded_func[0]
                func_params = decoded_func[1]
                
                if func_obj.fn_name == 'transfer':
                    # Extract raw params
                    recipient = func_params.get('_to')
                    raw_value = func_params.get('_value')
                    
                    # 4. Fetch Token Details to format amount
                    token_address = tx_data.get('to')
                    token_details = _get_token_meta(token_address)
                    
                    decimals = token_details['decimals']
                    symbol = token_details['symbol']
                    
                    formatted_amount = raw_value / (10 ** decimals)
                    
                    # 5. Inject formatted data into the response dict
                    tx_data['erc20_details'] = {
                        "is_transfer": True,
                        "token_address": token_address,
                        "token_symbol": symbol,
                        "token_decimals": decimals,
                        "amount_raw": raw_value,
                        "amount_formatted": formatted_amount,
                        "recipient": recipient,
                        "readable": f"Transfer {formatted_amount} {symbol} to {recipient}"
                    }
            except Exception as e:
                # Inject error if decoding specifically fails
                tx_data['decoding_debug_error'] = str(e)

        return json.dumps(tx_data)

    except Exception as e:
        return json.dumps({"error": f"General Failure: {str(e)}"})


def _get_token_meta(token_address):
    """Helper to get decimals/symbol with hardcoded fallbacks for major tokens to speed up response."""
    try:
        addr_lower = token_address.lower()
        # Fast path for USDT/USDC to avoid RPC calls
        if addr_lower == "0xdac17f958d2ee523a2206206994597c13d831ec7":
            return {"symbol": "USDT", "decimals": 6}
        if addr_lower == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48":
            return {"symbol": "USDC", "decimals": 6}
        
        # RPC path
        contract = w3.eth.contract(address=w3.to_checksum_address(token_address), abi=ERC20_ABI)
        decimals = contract.functions.decimals().call()
        symbol = contract.functions.symbol().call()
        return {"symbol": symbol, "decimals": decimals}
    except:
        return {"symbol": "Unknown", "decimals": 18} # Fallback

@mcp.tool
def eth_signature_decode_lookup(signature: str) -> str:
   r = requests.get(f"https://www.4byte.directory/api/v1/signatures/?hex_signature={signature}")
   return r.text

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
        "decimals": 18,
        "total_supply": 0
    }

    try: details["name"] = contract.functions.name().call()
    except: pass

    try: details["symbol"] = contract.functions.symbol().call()
    except: pass

    try: details["decimals"] = contract.functions.decimals().call()
    except: pass

    try:
        raw_supply = contract.functions.totalSupply().call()
        details["total_supply"] = raw_supply / (10 ** details["decimals"])
    except: pass

    return json.dumps(details, default=str)

@mcp.tool
def address_to_transactions(address: str) -> str:
    return "Not implemented"

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
        "context": get_addr_context(checksum_address)
    }
    return Web3.to_json(info)

if __name__ == "__main__":
    mcp.run()
