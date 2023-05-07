from flask import Flask, request
import json
from trade import MyCLient
from line_notify import LineNotify
from pprint import pprint
import os
from dotenv import load_dotenv
from database import db
import traceback

load_dotenv()

#__name__ -> app

app = Flask(__name__)

LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
line_notify = LineNotify(LINE_NOTIFY_TOKEN)

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
HOSTCLIENT = MyCLient(API_KEY, API_SECRET)
HOSTCLIENT.setup_class()
symbol_info = HOSTCLIENT.symbol_info

customers = list(db["customers"].find())

# # prepare customers clients
# for customer in customers:
#     api_key = customer["binance"]["api_key"]
#     secret_key = customer["binance"]["secret_key"]
#     testnet = customer["binance"]["testnet"]
#     customer["client"] = MyCLient(api_key, secret_key, testnet=testnet).create_client()

@app.route('/')
def main():
    return "Hello World"


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = json.loads(request.data.decode('utf-8'))

        buy_data = data["action"]
        isBuy = buy_data == "BUY"
        symbol = data["symbol"]
        
        for customer in customers:
            try:
                if customer["is_bot_on"] == False:
                    continue
                
                client = MyCLient(customer["binance"]["api_key"], customer["binance"]["secret_key"], testnet=customer["binance"]["testnet"])
                # client = customer["client"]
                success = client.rebalance(
                    isBuy,
                    symbol=symbol,
                    percent=0.6
                )
                if success:
                    price = client.client.get_symbol_ticker(symbol=symbol)["price"]
                    value = client.get_value_symbol(symbol)
                    symbol2 = symbol_info[symbol]["quoteAsset"]
                    message = f"RB {symbol} {buy_data}\n{symbol} {price:.2f} {symbol2}\nCurrent value: {value:.2f} {symbol2}"
                    line_notify.send(message)
            
            except:
                error_message = traceback.format_exc()
                print(error_message)
                line_notify.send(error_message)
                
    except:
        error_message = traceback.format_exc()
        print(error_message)
        line_notify.send(error_message)
        return "Error"

    return "OK"


# This is for local
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)