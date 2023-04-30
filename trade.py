from binance import Client
from pprint import pprint
import os
import dotenv

# load env
dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# testnet
API_KEY = "GRJaQlXdXyjHzKJv6uyfxIO1z7mTqq4QFzF0yFt4REJS1krN9lN2QipoDjfAg9lE"
SECRET_KEY = "J6rVvqYmHcSnQ6feekOxetR7WnCVGbDSt7qwzjJoUyMuBE6gpmb6Gb6Q6E9gfj7v"

# order = client.create_order(symbol=symbol,side="BUY",type="MARKET",quantity=qty)
# order = client.create_order(symbol=symbol,side="SELL",type="MARKET",quantity=qty)

# Diff at least 12 USDT that can be traded
MIN_DIFF_VALUE = 12
class MyCLient:
    def __init__(self, API_KEY, SECRET_KEY, testnet=False) -> None:
        self.client = Client(API_KEY, SECRET_KEY, testnet=testnet)
    def rebalance(self):
        pass
    
def create_client(API_KEY, SECRET_KEY, testnet=False):
    client = Client(API_KEY, SECRET_KEY, testnet=testnet)
    return client

def rebalance(client: Client,
              is_buy,
              symbol = "BTCUSDT",
              symbol1 = "BTC",
              symbol2 = "USDT",
              percent = None,
              target_value_symbol1 = None,
              target_value_symbol2 = None):
    if percent == None and target_value_symbol1 == None and target_value_symbol2 == None:
        percent = 0.5
    
    price_symbol1 = float(client.get_symbol_ticker(symbol=symbol)["price"])
    
    balance_symbol1 = float(client.get_asset_balance(asset=symbol1)["free"])
    balance_symbol2 = float(client.get_asset_balance(asset=symbol2)["free"])
    
    value_symbol1 = balance_symbol1 * price_symbol1
    value_symbol2 = balance_symbol2
    value_sum = value_symbol1 + value_symbol2
    
    if percent is not None:
        target_value_symbol1 = value_sum * percent
    else:
        if target_value_symbol1 is None and target_value_symbol2 is not None:
            target_value_symbol1 = value_sum - target_value_symbol2
    
    dif_quantity = abs(target_value_symbol1-value_symbol1)/(price_symbol1)
    dif_value = dif_quantity * price_symbol1
    
    if dif_value < MIN_DIFF_VALUE:
        print("Can't trade")
        print(f"Diff Value = {dif_value} {symbol2} < {MIN_DIFF_VALUE} {symbol2}")
        return False
    
    new_balance_symbol1 = balance_symbol1
    new_balance_symbol2 = balance_symbol2
    
    if target_value_symbol1 < value_symbol1 and not is_buy:
        new_balance_symbol1 -= dif_quantity
        new_balance_symbol2 += dif_value
        print(f"SELL {symbol1} {dif_quantity} [{dif_value} {symbol2}]")
        client.create_order(symbol=symbol,side="SELL",type="MARKET",quantity=dif_quantity)
    elif target_value_symbol1 > value_symbol1 and is_buy:
        new_balance_symbol1 += dif_quantity
        new_balance_symbol2 -= dif_value
        print(f"BUY {symbol1} {dif_quantity} [{dif_value} {symbol2}]")
        client.create_order(symbol=symbol,side="BUY",type="MARKET",quantity=dif_quantity)
    else:
        print("Do nothing")
        return False
    
    new_value_symbol1 = new_balance_symbol1 * price_symbol1
    new_value_symbol2 = new_balance_symbol2
    
    
    # region print
    print(f"Price {symbol1}/{symbol2} = {price_symbol1} {symbol2}")
    print(f"Balance {symbol1} = {balance_symbol1} {symbol1}\nBalance {symbol2} = {balance_symbol2} {symbol2}")
    print(f"Value {symbol1} = {value_symbol1} {symbol2}\nValue {symbol2} = {value_symbol2} {symbol2}\nSum = {value_sum} {symbol2}")
    print(f"Percent = {percent}\nTarget Value {symbol1} = {target_value_symbol1} {symbol2}")
    if not is_buy:
        print(f"SELL {symbol1} {dif_quantity} [{dif_value} {symbol2}]")
    else:
        print(f"BUY {symbol1} {dif_quantity} [{dif_value} {symbol2}]")
    
    print(f"Balance {symbol1} = {new_balance_symbol1} {symbol1}\nBalance {symbol2} = {new_balance_symbol2} {symbol2}")
    print(f"Value {symbol1} = {new_value_symbol1} {symbol2}\nValue {symbol2} = {new_value_symbol2} {symbol2}")
    # endregion
    return True

def get_symbols_info(client):
    exchange_info = client.get_exchange_info()
    exchange_info2 = {}
    for i in exchange_info["symbols"]:
        exchange_info2[i["symbol"]] = {
            "baseAsset": i["baseAsset"],
            "quoteAsset": i["quoteAsset"],
        }
    return exchange_info2

def get_value_symbol(client, symbol="BTCUSDT", symbol1="BTC", symbol2="USDT"):
    price_symbol1 = float(client.get_symbol_ticker(symbol=symbol)["price"])
    balance_symbol1 = float(client.get_asset_balance(asset=symbol1)["free"])
    balance_symbol2 = float(client.get_asset_balance(asset=symbol2)["free"])
    value_symbol1 = balance_symbol1 * price_symbol1
    value_symbol2 = balance_symbol2
    value_symbol = value_symbol1 + value_symbol2
    return value_symbol

if __name__ == "__main__":
    client = create_client(API_KEY=API_KEY, SECRET_KEY=SECRET_KEY, testnet=True)
    # pprint(get_symbols_info(client))
    # rebalance(client, False, percent=0.5)
    pprint(client.get_account())