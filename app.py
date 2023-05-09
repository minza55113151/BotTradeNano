from flask import Flask, request
import json
from trade import MyCLient
from line_notify import LineNotify
from pprint import pprint
import os
from dotenv import load_dotenv
from database.database import DB
import traceback

load_dotenv()

#__name__ -> app

app = Flask(__name__)

LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
line_notify = LineNotify(LINE_NOTIFY_TOKEN)
line_notify.send("Server online")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
HOSTCLIENT = MyCLient(API_KEY, API_SECRET)
HOSTCLIENT.setup_class()
symbol_info = HOSTCLIENT.symbol_info

customers = DB.get_customers()

# prepare customers clients
for customer in customers:
    api_key = customer["binance"]["api_key"]
    secret_key = customer["binance"]["secret_key"]
    testnet = customer["binance"]["testnet"]
    customer["client"] = MyCLient(api_key, secret_key, testnet=testnet).create_client()

# VPS

@app.route('/')
def main():
    line_notify.send("Hello World")
    return "Hello World"


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = json.loads(request.data.decode('utf-8'))

        bot_name = data["bot_name"]

        buy_data = data["action"]
        isBuy = buy_data == "BUY"
        symbol = data["symbol"]
        
        for customer in customers:
            try:
                if not customer["is_bot_on"] or not customer["bot"][bot_name]:
                    continue
                
                client = customer["client"]
                success = client.rebalance(
                    isBuy,
                    symbol=symbol,
                    percent=0.6
                )
                if success:
                    price = float(client.client.get_symbol_ticker(symbol=symbol)["price"])
                    value = client.get_value_symbol(symbol)
                    
                    symbol2 = client.get_symbols_info()[symbol]["quoteAsset"]
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