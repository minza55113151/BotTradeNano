import os
from dotenv import load_dotenv
from trade import MyCLient

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
HOSTCLIENT = MyCLient(API_KEY, API_SECRET)
HOSTCLIENT.setup_class()
print(HOSTCLIENT.symbol_info)