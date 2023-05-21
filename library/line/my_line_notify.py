from line_notify import LineNotify
import os


class MyLineNotify:
    SERVER_TOKEN = ""
    @staticmethod
    def send(token: str, message: str) -> None:
        line_notify = LineNotify(token)
        return line_notify.send(message)
        
        
    @staticmethod
    def server_send(message: str) -> None:
        return MyLineNotify.send(MyLineNotify.SERVER_TOKEN, message)


LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
MyLineNotify.SERVER_TOKEN = LINE_NOTIFY_TOKEN