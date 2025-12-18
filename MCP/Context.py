import pandas as pd
import requests

def get_context(addr):
    df = pd.read_csv("eth_addresses.csv")
    return df.loc[df["Address"] == addr].to_dict(orient="records")[0] if addr in df["Address"].values else {}

def get_context_api(addr):
    url = f"https://eth-labels-production.up.railway.app/labels/{addr}"
    response = requests.get(url)
    try:
        return response.json()[0]
    except IndexError:
        return {}

