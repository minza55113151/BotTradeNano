from pymongo import typings
{
    "_id": typings.ObjectId,
    "info": {
        "name": str,
    },
    "broker": "str",
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
    "bots": {
        "NANO": {
            "is_on": bool,
            "symbol": str,
            "percent": float,
            "target_value_symbol1": float,
            "target_value_symbol2": float,
            "is_notify": bool,
        },
    },
    "line": {
        "token": str,
        "is_notify": bool,
    }
}