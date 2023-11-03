from flask import Flask, request, jsonify
import redis
from os import getenv
import random
from alpha_vantage.timeseries import TimeSeries

app = Flask(__name__)

class Config:
    alpha_api_key = getenv("ALPHA_VANTAGE_API_KEY", None)
    port = int(getenv("STOCK_API_PORT", None))
    redis_port = int(getenv("REDIS_PORT"))
    verbose = getenv("VERBOSE", "true").lower() in ("true", "1")
    replica_id = random.randint(1, 9999)

# Connect to Redis
redis_client = redis.StrictRedis(host='redis-service', port=Config.redis_port, decode_responses=True)

@app.route('/get_price', methods=['GET'])
def get_price():
    stock_symbol = request.args.get('symbol')
    if not stock_symbol:
        return jsonify({'error': 'Symbol not provided'}), 400

    try:
        if Config.alpha_api_key is None:
            return jsonify({'error': 'ALPHA_VANTAGE_API_KEY is not set'}), 400

        # Check if the price is in the cache
        cached_price = redis_client.get(stock_symbol)
        if cached_price is not None:
            return jsonify({'price': cached_price, 'replica_id': Config.replica_id, 'from_redis': True})

        # If not in the cache, call the API and store it in Redis
        ts = TimeSeries(key=Config.alpha_api_key)
        resp = ts.get_intraday(stock_symbol, interval='1min')[0]
        price = list(resp.values())[0]['4. close']

        # Store the price in Redis with a 2-minute expiration
        redis_client.setex(stock_symbol, 180, price)

        return jsonify({'price': price, 'replica_id': Config.replica_id, 'from_redis': False})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=Config.port)