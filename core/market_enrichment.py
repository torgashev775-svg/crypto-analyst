import requests

def coin_price(coin_id: str):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd")
        return r.json()
    except Exception:
        return {}

def whale_transfers(coin: str):
    return {}
