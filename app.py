from flask import Flask, request
import json
from trade import create_client, rebalance
from line_notify import LineNotify

app = Flask(__name__)

LINE_NOTIFY_TOKEN = "MiGiGvEehvIskk3qJrXLFeQ78Adpf9UvLO2wGLgA9JP"
line_notify = LineNotify(LINE_NOTIFY_TOKEN)

customers = [
    {
        "id": 0,
        "binance": {
            "api_key": "GRJaQlXdXyjHzKJv6uyfxIO1z7mTqq4QFzF0yFt4REJS1krN9lN2QipoDjfAg9lE",
            "secret_key": "J6rVvqYmHcSnQ6feekOxetR7WnCVGbDSt7qwzjJoUyMuBE6gpmb6Gb6Q6E9gfj7v"
        },
        "bitkub": {}
    }
]

@app.route('/')
def main():
    return "Working!!!"


@app.route('/webhook', methods=['POST'])
def webhook():
    signal = request.data.decode('utf-8')
    signal = json.loads(signal)
    
    print(signal)
    
    buy_signal = signal["ACTION"]
    symbol = signal["SYMBOL"]
    amount_coin = float(signal["AMOUNT_COIN"])
    leverage = int(signal["LEV"])
    
    message = f"buy_signal: {buy_signal}\nsymbol: {symbol}\namount_coin: {amount_coin}\nleverage: {leverage}"
    print(message)
    line_notify.send(message)
    
    for customer in customers:
        print(customer["id"])
        client = create_client(customer["api_key"], customer["secret_key"], testnet=True)
        # rebalance(
        #     client,
        #     buy_signal,
        #     symbol1=signal['SYMBOL'],
        #     percent=float(signal['AMOUNT_COIN'])
        #     )



    return "Webhook is working!!!"

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=8000)
    pass
    
    
# @app.route("/signals",methods=['POST'])
# def signals():
#     print("Someone Post Signals to me !")
#     signal = request.data.decode("utf-8")
#     import json
#     signal = json.loads(signal) # เปลี่ยนจาก json ให้เป็น dictionary

#     trade_side = signal["ACTION"]
#     amount_coin = float(signal["AMOUNT_COIN"])
#     leverage = int(signal["LEV"])
#     symbol = signal["SYMBOL"]

#     print("ได้รับสัญญาณการซื้อขาย ดังนี้.....")
#     print(trade_side)
#     print(amount_coin)
#     print(leverage)
#     print(symbol)
#     print("บอทเริ่มทำคำสั่งซื้อขายอัตโนมัติ ไปที่ ไบแนน.....")

#     message = f"🤖🤖🤖🤖🤖🤖🤖\n🤖ได้รับสัญญาณการซื้อขาย ดังนี้..... \n🤖รูปแบบการเทรด {trade_side} {symbol}\n🤖จำนวนที่เปิด {amount_coin} \n🤖LEVERAGE {leverage}\n🤖🤖🤖🤖🤖🤖🤖"
#     # Line notify Process
#     
#     Access_Token = "bYMefbv4lFK3Bn5esd45e8SqVmw78oHsqL9LrIVQ2DZ" # generate line notify
#     notify = LineNotify(Access_Token)
#     notify.send(message) # ส่งไปที่ห้องแชท


#     return "200"    