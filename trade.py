from binance import Client
from binance.helpers import round_step_size
from database.database import DB


class MyClient:
    symbols_info = None
    
    #region setup
    def __init__(self, API_KEY, SECRET_KEY, testnet=False) -> None:
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.testnet = testnet
        
        self._client = None

    def create_client(self):
        self._client = Client(self.API_KEY, self.SECRET_KEY, testnet=self.testnet)
        return self
    #endregion
    
    #region get
    def get_client(self):
        if self._client is None:
            self.create_client()
            
        return self._client

    def get_symbols_info(self):
        if MyClient.symbols_info:
            return MyClient.symbols_info
        
        client = self.get_client()
        
        exchange_info = client.get_exchange_info()
        symbols_info = {}
        for i in exchange_info["symbols"]:
            symbols_info[i["symbol"]] = {
                "baseAsset": i["baseAsset"],
                "quoteAsset": i["quoteAsset"],
                "filters": i["filters"],
            }
            
        if not self.testnet:
            MyClient.symbols_info = symbols_info
            
        return symbols_info
       
    def get_value_symbol(self, symbol):
        if not symbol:
            return None
        
        client = self.get_client()
        symbols_info = self.get_symbols_info()
        
        symbol1 = symbols_info[symbol]["baseAsset"]
        symbol2 = symbols_info[symbol]["quoteAsset"]
        price_symbol1 = float(client.get_symbol_ticker(symbol=symbol)["price"])
        balance_symbol1 = float(client.get_asset_balance(asset=symbol1)["free"])
        balance_symbol2 = float(client.get_asset_balance(asset=symbol2)["free"])
        value_symbol1 = balance_symbol1 * price_symbol1
        value_symbol2 = balance_symbol2
        value_symbol = value_symbol1 + value_symbol2
        
        return value_symbol
    
    def get_data_to_rebalance(self, symbol, percent=None, target_value_symbol1=None, target_value_symbol2=None):
        client = self.get_client()
        symbols_info = self.get_symbols_info()
        
        symbol1 = symbols_info[symbol]["baseAsset"]
        symbol2 = symbols_info[symbol]["quoteAsset"]
        
        min_qty = float(symbols_info[symbol]["filters"][1]["minQty"])
        step_size = float(symbols_info[symbol]["filters"][1]["stepSize"])
        
        price_symbol1 = float(client.get_symbol_ticker(symbol=symbol)["price"])
        balance_symbol1 = float(client.get_asset_balance(asset=symbol1)["free"])
        balance_symbol2 = float(client.get_asset_balance(asset=symbol2)["free"])
        
        value_symbol1 = balance_symbol1 * price_symbol1
        value_symbol2 = balance_symbol2
        value_sum = value_symbol1 + value_symbol2

        if percent == None and target_value_symbol1 == None and target_value_symbol2 == None:
            percent = 0.5
        
        if percent is not None:
            target_value_symbol1 = value_sum * percent
        else:
            if target_value_symbol1 is None and target_value_symbol2 is not None:
                target_value_symbol1 = value_sum - target_value_symbol2
        
        dif_quantity = abs(target_value_symbol1-value_symbol1)/(price_symbol1)
        dif_quantity = round_step_size(dif_quantity, step_size)
        dif_value = dif_quantity * price_symbol1
        
        return {
            "symbol": symbol,
            "symbol1": symbol1,
            "symbol2": symbol2,
            "price_symbol1": price_symbol1,
            "balance_symbol1": balance_symbol1,
            "balance_symbol2": balance_symbol2,
            "value_symbol1": value_symbol1,
            "value_symbol2": value_symbol2,
            "value_sum": value_sum,
            "percent": percent,
            "target_value_symbol1": target_value_symbol1,
            "target_value_symbol2": target_value_symbol2,
            "dif_quantity": dif_quantity,
            "dif_value": dif_value,
            "min_qty": min_qty,
            "step_size": step_size,
        }
    #endregion
    
    def rebalance(
        self,
        customer_id: str,
        bot_name: str,
        is_buy: bool,
        symbol: str,
        percent: float = None,
        target_value_symbol1: float = None,
        target_value_symbol2: float = None,
        is_test: bool = False,
        is_print: bool = False
    ) -> bool:
        client = self.get_client()
        
        data = self.get_data_to_rebalance(
            symbol=symbol,
            percent=percent,
            target_value_symbol1=target_value_symbol1,
            target_value_symbol2=target_value_symbol2
        )
        
        symbol = data["symbol"]
        symbol1 = data["symbol1"]
        symbol2 = data["symbol2"]
        price_symbol1 = data["price_symbol1"]
        balance_symbol1 = data["balance_symbol1"]
        balance_symbol2 = data["balance_symbol2"]
        value_symbol1 = data["value_symbol1"]
        value_symbol2 = data["value_symbol2"]
        value_sum = data["value_sum"]
        percent = data["percent"]
        target_value_symbol1 = data["target_value_symbol1"]
        target_value_symbol2 = data["target_value_symbol2"]
        dif_quantity = data["dif_quantity"]
        dif_value = data["dif_value"]
        min_qty = data["min_qty"]
        step_size = data["step_size"]
        
        new_balance_symbol1 = balance_symbol1
        new_balance_symbol2 = balance_symbol2
        
        if dif_quantity < min_qty:
            if is_print:
                print(f"Can't trade diff quantity = {dif_quantity} {symbol1} < {min_qty} {symbol1}")
            return False
        
        if target_value_symbol1 < value_symbol1 and not is_buy:
            new_balance_symbol1 -= dif_quantity
            new_balance_symbol2 += dif_value
            if not is_test:
                client.create_order(symbol=symbol,side="SELL",type="MARKET",quantity=dif_quantity)
                DB.log_trade({
                    "customer_id": customer_id,
                    "bot_name": bot_name,
                    "symbol": symbol,
                    "side": "SELL",
                    "type": "MARKET",
                    "quantity": dif_quantity,
                    "price": price_symbol1,
                    "value": dif_value,
                    "balance_symbol1": balance_symbol1,
                    "balance_symbol2": balance_symbol2,
                    "value_symbol1": value_symbol1,
                    "value_symbol2": value_symbol2,
                    "value_sum": value_sum,
                    "percent": percent,
                    "target_value_symbol1": target_value_symbol1,
                    "target_value_symbol2": target_value_symbol2,
                })
        elif target_value_symbol1 > value_symbol1 and is_buy:
            new_balance_symbol1 += dif_quantity
            new_balance_symbol2 -= dif_value
            if not is_test:
                client.create_order(symbol=symbol,side="BUY",type="MARKET",quantity=dif_quantity)
                DB.log_trade({
                    "customer_id": customer_id,
                    "bot_name": bot_name,
                    "symbol": symbol,
                    "side": "BUY",
                    "type": "MARKET",
                    "quantity": dif_quantity,
                    "price": price_symbol1,
                    "value": dif_value,
                    "balance_symbol1": balance_symbol1,
                    "balance_symbol2": balance_symbol2,
                    "value_symbol1": value_symbol1,
                    "value_symbol2": value_symbol2,
                    "value_sum": value_sum,
                    "percent": percent,
                    "target_value_symbol1": target_value_symbol1,
                    "target_value_symbol2": target_value_symbol2,
                })
        else:
            if is_print:
                print("Do nothing")
            return False

        if is_print:
            print(f"Price {symbol1}/{symbol2} = {price_symbol1} {symbol2}")
            print(f"Balance {symbol1} = {balance_symbol1} {symbol1}\nBalance {symbol2} = {balance_symbol2} {symbol2}")
            print(f"Value {symbol1} = {value_symbol1} {symbol2}\nValue {symbol2} = {value_symbol2} {symbol2}\nSum = {value_sum} {symbol2}")
            print(f"Percent = {percent}\nTarget Value {symbol1} = {target_value_symbol1} {symbol2}")
            if not is_buy:
                print(f"SELL {symbol1} {dif_quantity} [{dif_value} {symbol2}]")
            else:
                print(f"BUY {symbol1} {dif_quantity} [{dif_value} {symbol2}]")
            print(f"Balance {symbol1} = {new_balance_symbol1} {symbol1}\nBalance {symbol2} = {new_balance_symbol2} {symbol2}")
        
        return True 


if __name__ == "__main__":
    pass