import pandas as pd
import requests

def get_addr_context(addr):
    df = pd.read_csv("eth_addresses.csv")
    return df.loc[df["Address"] == addr].to_dict(orient="records")[0] if addr in df["Address"].values else {}

def get_addr_context_api(addr):
    url = f"https://eth-labels-production.up.railway.app/labels/{addr}"
    response = requests.get(url)
    try:
        return response.json()[0]
    except IndexError:
        return {}

def get_tx_context_api(tx_hash):
    # curl 'https://eth-labels-production.up.railway.app/accounts?address=0x02331657f38d44c30b4485f0f6312274bd5af1c1'
    url = f"https://eth-labels-production.up.railway.app/accounts?address={tx_hash}"
    response = requests.get(url)
    try:
        return response.json()[0]
    except IndexError:
        return {}

