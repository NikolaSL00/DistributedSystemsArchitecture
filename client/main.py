import requests
import time
import random
from datetime import datetime

server_url = 'http://example.com:30080'

def get_price(symbol):
    try:
        response = requests.get(f'{server_url}/get_price?symbol={symbol}')
        response_data = response.json()

        return response_data
    except:
        return {}

while True:
    symbol = random.choice(["TSLA", "AAPL", "MSFT", "GOOG", "IBM"])
    res = get_price(symbol)
    if 'price' in res:
        print(f"[{datetime.now()}] {symbol}: {res['price']}, replica_id:{res['replica_id']}, from redis: {res['from_redis']}", flush=True)
    else:
        print("Error connecting to the server")
    time.sleep(1)