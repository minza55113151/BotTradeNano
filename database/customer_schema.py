from pymongo import typings
{
    "_id": typings.ObjectId,
    # "broker": "str",
    "binance": {
        "api_key": str,
        "secret_key": str,
        "testnet": bool,
    },
    "bitkub":{
        # "api_key": str,
        # "secret_key": str,
    },
    "is_bot_on": bool,
    "bot": {
        "CDC": bool,
        "NANO": bool,
        # "CDC": {
        #     "is_on": bool,
        #     "symbol": str,
        #     "percent": float,
        #     "target_value_symbol1": float,
        #     "target_value_symbol2": float,
        #     "is_notify": bool,
        # },
        # "NANO": {
        #     "is_on": bool,
        #     "symbol": str,
        #     "percent": float,
        #     "target_value_symbol1": float,
        #     "target_value_symbol2": float,
        #     "is_notify": bool,
        # },
    },
    # "line": {
    #     "token": str,
    #     "is_notify": bool?
    # }
}