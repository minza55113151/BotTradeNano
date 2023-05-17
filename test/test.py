import sys, os
from dotenv import load_dotenv
from pprint import pprint

print(os.getcwd())
sys.path.append(os.path.join(os.getcwd()))

from trade import MyClient

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
HOSTCLIENT = MyClient(API_KEY, API_SECRET).create_client()
pprint(HOSTCLIENT.get_symbols_info()["ETHUSDT"])