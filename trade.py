from binance import Client
from pprint import pprint
import os
import dotenv

# # load env
# dotenv.load_dotenv()
# API_KEY = os.getenv('API_KEY')
# SECRET_KEY = os.getenv('SECRET_KEY')

API_KEY="GRJaQlXdXyjHzKJv6uyfxIO1z7mTqq4QFzF0yFt4REJS1krN9lN2QipoDjfAg9lE"
SECRET_KEY="J6rVvqYmHcSnQ6feekOxetR7WnCVGbDSt7qwzjJoUyMuBE6gpmb6Gb6Q6E9gfj7v"

# order = client.create_order(symbol=symbol,side='BUY',type='MARKET',quantity=qty)
# order = client.create_order(symbol=symbol,side='SELL',type='MARKET',quantity=qty)


def create_client(API_KEY, SECRET_KEY):
    client = Client(API_KEY, SECRET_KEY, testnet=True)
    return client

def rebalance(client, symbol1 = 'USDT', symbol2 = 'BTC'):
    balance1 = client.get_asset_balance(asset=symbol1)
    balance2 = client.get_asset_balance(asset=symbol2)
    print(balance1)
    print(balance2)
    #get price of symbol1
    # price1 = client.get_symbol_ticker(symbol=symbol1)
    
client = create_client(API_KEY=API_KEY, SECRET_KEY=SECRET_KEY)
rebalance(client)