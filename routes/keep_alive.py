from flask import Blueprint
from datetime import datetime, timezone, timedelta
from library.line.my_line_notify import MyLineNotify


keep_alive = Blueprint("keep_alive", __name__)


@keep_alive.route("/")
def main():
    datetime_now = datetime.utcnow() + timedelta(hours=7)

    if datetime_now.hour == 0 and datetime_now.minute <= 5:
        MyLineNotify.server_send("Keep Alive")
        
    return "OK"