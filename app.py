from flask import Flask, request
import json
from trade import create_client, rebalance, get_value_symbol, get_symbols_info
from line_notify import LineNotify
from pprint import pprint

app = Flask(__name__)

LINE_NOTIFY_TOKEN = "MiGiGvEehvIskk3qJrXLFeQ78Adpf9UvLO2wGLgA9JP"
line_notify = LineNotify(LINE_NOTIFY_TOKEN)


customers = [
    {
        "id": 0,
        "binance": {
            "api_key": "GRJaQlXdXyjHzKJv6uyfxIO1z7mTqq4QFzF0yFt4REJS1krN9lN2QipoDjfAg9lE",
            "secret_key": "J6rVvqYmHcSnQ6feekOxetR7WnCVGbDSt7qwzjJoUyMuBE6gpmb6Gb6Q6E9gfj7v",
            "testnet": True
        },
        "bitkub": {}
    }
]


HOSTCLIENT = create_client("GRJaQlXdXyjHzKJv6uyfxIO1z7mTqq4QFzF0yFt4REJS1krN9lN2QipoDjfAg9lE", "J6rVvqYmHcSnQ6feekOxetR7WnCVGbDSt7qwzjJoUyMuBE6gpmb6Gb6Q6E9gfj7v", testnet=True)
symbol_info = get_symbols_info(HOSTCLIENT)

@app.route('/')
def main():
    return "Working!!!"


@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data.decode('utf-8'))

    buy_data = data["action"]
    isBuy = buy_data == "BUY"
    symbol = data["symbol"]
    
    print("------------------")
    print(f"Rebalance {symbol} {buy_data}")
    pprint(data)
    print("------------------")
    
    for customer in customers:
        client = create_client(customer["binance"]["api_key"], customer["binance"]["secret_key"], testnet=customer["binance"]["testnet"])
        success = rebalance(
            client,
            isBuy,
            symbol=symbol,
            symbol1=symbol_info[symbol]["baseAsset"],
            symbol2=symbol_info[symbol]["quoteAsset"],
            percent=0.5
        )
        if success:
            value = get_value_symbol(client, symbol, symbol_info[symbol]["baseAsset"], symbol_info[symbol]["quoteAsset"])
            message = f"Rebalance {symbol} {buy_data}\nValue: {value}"
            line_notify.send(message)

    return "Webhook is working!!!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)