from flask import Flask

from routes.test import test
from routes.keep_alive import keep_alive
from routes.webhook import webhook


# VPS


app = Flask(__name__)

app.register_blueprint(test, url_prefix="/test")
app.register_blueprint(keep_alive, url_prefix="/keep-alive")
app.register_blueprint(webhook, url_prefix="/webhook")

@app.route("/")
def main():
    return "Hello World"


# @app.route("/webhook", methods=["POST"])
# def webhook():
#     try:
#         data = json.loads(request.data.decode("utf-8"))

#         bot_name = data["bot_name"]

#         buy_data = data["action"]
#         isBuy = buy_data == "BUY"
#         symbol = data["symbol"]
        
#         DB.log_alert(data)
        
#         for customer in customers:
#             try:
#                 is_bot_on = customer["is_bot_on"] and customer["bots"][bot_name]["is_on"]
#                 if not is_bot_on: continue
                
#                 customer_symbol = customer["bots"][bot_name]["symbol"]
#                 if symbol != customer_symbol: continue
                
#                 client: MyClient = customer["client"]
#                 success = client.rebalance(
#                     customer["_id"],
#                     bot_name,
#                     isBuy,
#                     symbol,
#                     percent=customer["bots"][bot_name]["percent"],
#                     target_value_symbol1=customer["bots"][bot_name]["target_value_symbol1"],
#                     target_value_symbol2=customer["bots"][bot_name]["target_value_symbol2"],
#                 )
                
#                 if not success: continue
                
#                 if customer["bots"][bot_name]["is_notify"] and customer["line"]["is_notify"]:
#                     price = float(client._client.get_symbol_ticker(symbol=symbol)["price"])
#                     value = client.get_value_symbol(symbol)
#                     symbol2 = client.get_symbols_info()[symbol]["quoteAsset"]
#                     customer_name = customer["info"]["name"]
#                     message = f"Name:{customer_name} BOT:{bot_name} {symbol} {buy_data}\n{symbol} {price:.2f} {symbol2}\nValue: {value:.2f} {symbol2}"
                    
#                     # line_token_key = customer["line"]["token_key"]
#                     # MyLineNotify.send(line_token_key, message)
                    
#                     MyLineNotify.server_send(message)
                
#             except:
#                 error_message = traceback.format_exc()
#                 print(error_message)
#                 MyLineNotify.server_send(error_message)
                
#     except:
#         error_message = traceback.format_exc()
#         print(error_message)
#         MyLineNotify.server_send(error_message)
#         return "Error"

#     return "OK"


# This is for local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)