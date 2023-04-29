from flask import Flask, request
import json
from trade import create_client, rebalance
from line_notify import LineNotify

app = Flask(__name__)

LINE_NOTIFY_TOKEN = "MiGiGvEehvIskk3qJrXLFeQ78Adpf9UvLO2wGLgA9JP"
line_notify = LineNotify(LINE_NOTIFY_TOKEN)

customers = [
    {
        "id": 0,
        "binance": {
            "api_key": "GRJaQlXdXyjHzKJv6uyfxIO1z7mTqq4QFzF0yFt4REJS1krN9lN2QipoDjfAg9lE",
            "secret_key": "J6rVvqYmHcSnQ6feekOxetR7WnCVGbDSt7qwzjJoUyMuBE6gpmb6Gb6Q6E9gfj7v"
        },
        "bitkub": {}
    }
]

@app.route('/')
def main():
    return "Working!!!"


@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data.decode('utf-8'))
    
    print(data)
    
    buy_data = data["action"]
    isBuy = buy_data == "BUY"
    
    symbol = data["symbol"]
    amount_coin = float(data["amount_coin"])
    leverage = int(data["lev"])
    
    message = data
    print(message)
    line_notify.send(str(message))
    
    for customer in customers:
        print(customer["id"])
        client = create_client(customer["binance"]["api_key"], customer["binance"]["secret_key"], testnet=True)
        # rebalance(
        #     client,
        #     buy_data,
        #     symbol1=data['SYMBOL'],
        #     percent=float(data['AMOUNT_COIN'])
        #     )



    return "Webhook is working!!!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)