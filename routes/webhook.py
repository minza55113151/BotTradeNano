from flask import Blueprint, request
import json
import traceback
from dotenv import load_dotenv
from library.trade.trade import MyClient
from library.line.my_line_notify import MyLineNotify
from database.database import DB
load_dotenv()


class Customers:
    is_create_client = False
    customers = DB.get_customers()
    
    @staticmethod
    def get_customers() -> list:
        if not Customers.is_create_client:
            Customers.create_customer_client()
        return Customers.customers
    
    @staticmethod
    def create_customer_client() -> None:
        for customer in Customers.customers:
            broker = customer["broker"]
            api_key = customer[broker]["api_key"]
            secret_key = customer[broker]["secret_key"]
            testnet = customer[broker]["testnet"]
            customer["client"] = MyClient(api_key, secret_key, testnet=testnet).create_client()
        Customers.is_create_client = True


class WebHook:
    def __init__(self) -> None:
        pass
    
    def on_data_received(self, data) -> str:        
        try:
            bot_name = data["bot_name"]
            
            buy_data = data["action"]
            isBuy = buy_data == "BUY"
            symbol = data["symbol"]
            
            DB.log_alert(data)
            
            self.execute_bot(bot_name, isBuy, symbol)
        except:
            self.error_handler()
            
            return "Error"
        
        return "OK"
    
    def execute_bot(self, bot_name, isBuy, symbol) -> None:
        for customer in Customers.customers:
            try:
                self.execute_bot_for_each_customer(customer, bot_name, isBuy, symbol)
            except:
               self.error_handler()
        
    def execute_bot_for_each_customer(self, customer, bot_name, isBuy, symbol) -> None:
        is_bot_on = customer["is_bot_on"] and customer["bots"][bot_name]["is_on"]
        if not is_bot_on: return
        
        # TODO: symbol in customer_symbols
        customer_symbol = customer["bots"][bot_name]["symbol"]
        if symbol != customer_symbol: return
        
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
        
        if not success: return
        
        if customer["bots"][bot_name]["is_notify"] and customer["line"]["is_notify"]:
            price = float(client._client.get_symbol_ticker(symbol=symbol)["price"])
            value = client.get_value_symbol(symbol)
            symbol2 = client.get_symbols_info()[symbol]["quoteAsset"]
            customer_name = customer["info"]["name"]
            message = f"Name:{customer_name} BOT:{bot_name} {symbol} {isBuy}\n{symbol} {price:.2f} {symbol2}\nValue: {value:.2f} {symbol2}"
            
            line_token_key = customer["line"]["token_key"]
            MyLineNotify.send(line_token_key, message)

    def error_handler(self) -> None:
        error_message = traceback.format_exc()
        print(error_message)
        MyLineNotify.server_send(error_message)



webhook = Blueprint("webhook", __name__)


@webhook.route("/", methods=["POST"])
def webhook():
    data = json.loads(request.data.decode("utf-8"))
    return WebHook().on_data_received(data)
    # try:

    #     bot_name = data["bot_name"]

    #     buy_data = data["action"]
    #     isBuy = buy_data == "BUY"
    #     symbol = data["symbol"]
        
    #     DB.log_alert(data)
        
    #     for customer in customers:
    #         try:
    #             is_bot_on = customer["is_bot_on"] and customer["bots"][bot_name]["is_on"]
    #             if not is_bot_on: continue
                
    #             customer_symbol = customer["bots"][bot_name]["symbol"]
    #             if symbol != customer_symbol: continue
                
    #             client: MyClient = customer["client"]
    #             success = client.rebalance(
    #                 customer["_id"],
    #                 bot_name,
    #                 isBuy,
    #                 symbol,
    #                 percent=customer["bots"][bot_name]["percent"],
    #                 target_value_symbol1=customer["bots"][bot_name]["target_value_symbol1"],
    #                 target_value_symbol2=customer["bots"][bot_name]["target_value_symbol2"],
    #             )
                
    #             if not success: continue
                
    #             if customer["bots"][bot_name]["is_notify"] and customer["line"]["is_notify"]:
    #                 price = float(client._client.get_symbol_ticker(symbol=symbol)["price"])
    #                 value = client.get_value_symbol(symbol)
    #                 symbol2 = client.get_symbols_info()[symbol]["quoteAsset"]
    #                 customer_name = customer["info"]["name"]
    #                 message = f"Name:{customer_name} BOT:{bot_name} {symbol} {buy_data}\n{symbol} {price:.2f} {symbol2}\nValue: {value:.2f} {symbol2}"
                    
    #                 line_token_key = customer["line"]["token_key"]
    #                 MyLineNotify.send(line_token_key, message)
                
    #         except:
    #             error_message = traceback.format_exc()
    #             print(error_message)
    #             MyLineNotify.server_send(error_message)
                
    # except:
    #     error_message = traceback.format_exc()
    #     print(error_message)
    #     MyLineNotify.server_send(error_message)
    #     return "Error"

    # return "OK"
