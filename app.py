from flask import Flask, request
import json
from trade import MyClient
from line_notify import LineNotify
from pprint import pprint
import os
from dotenv import load_dotenv
from database.database import DB
import traceback
from datetime import datetime, timezone, timedelta
load_dotenv()


LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
SERVER_LINE = LineNotify(LINE_NOTIFY_TOKEN)

customers = DB.get_customers()

for customer in customers:
    broker = customer["broker"]
    api_key = customer[broker]["api_key"]
    secret_key = customer[broker]["secret_key"]
    testnet = customer[broker]["testnet"]
    customer["client"] = MyClient(api_key, secret_key, testnet=testnet).create_client()

# VPS


app = Flask(__name__)


@app.route("/")
def main():
    return "Hello World"


@app.route("/keep-alive")
def keep_alive():
    datetime_now = datetime.now(tz=timezone(timedelta(hours=7)))
    if datetime_now.hour == 0 and datetime_now.minute <= 5:
        SERVER_LINE.send("Keep Alive")
        
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = json.loads(request.data.decode("utf-8"))

        bot_name = data["bot_name"]

        buy_data = data["action"]
        isBuy = buy_data == "BUY"
        symbol = data["symbol"]
        
        DB.log_alert(data)
        
        for customer in customers:
            try:
                is_bot_on = customer["is_bot_on"] and customer["bots"][bot_name]["is_on"]
                if not is_bot_on: continue
                
                customer_symbol = customer["bots"][bot_name]["symbol"]
                if symbol != customer_symbol: continue
                
                client: MyClient = customer["client"]
                success = client.rebalance(
                    customer["_id"],
                    bot_name,
                    isBuy,
                    symbol,
                    percent=customer["bots"][bot_name]["percent"],
                    target_value_symbol1=customer["bots"][bot_name]["target_value_symbol1"],
                    target_value_symbol2=customer["bots"][bot_name]["target_value_symbol2"],
                )
                
                if not success: continue
                
                if customer["bots"][bot_name]["is_notify"] and customer["line"]["is_notify"]:
                    price = float(client.client.get_symbol_ticker(symbol=symbol)["price"])
                    value = client.get_value_symbol(symbol)
                    symbol2 = client.get_symbols_info()[symbol]["quoteAsset"]
                    customer_name = customer["info"]["name"]
                    message = f"Name:{customer_name} BOT:{bot_name} {symbol} {buy_data}\n{symbol} {price:.2f} {symbol2}\nValue: {value:.2f} {symbol2}"
                    
                    # line_token_key = customer["line"]["token_key"]
                    # line_notify = LineNotify(line_token_key)
                    # line_notify.send(message)
                    
                    SERVER_LINE.send(message)
                
            except:
                error_message = traceback.format_exc()
                print(error_message)
                SERVER_LINE.send(error_message)
                
    except:
        error_message = traceback.format_exc()
        print(error_message)
        SERVER_LINE.send(error_message)
        return "Error"

    return "OK"


# This is for local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)