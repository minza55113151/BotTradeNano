from flask import Flask
from waitress import serve
from paste.translogger import TransLogger

from routes.test import test
from routes.keep_alive import keep_alive
from routes.webhook import webhook


app = Flask(__name__)

app.register_blueprint(test, url_prefix="/test")
app.register_blueprint(keep_alive, url_prefix="/keep-alive")
app.register_blueprint(webhook, url_prefix="/webhook")

@app.route("/")
def main():
    return "Hello World"


if __name__ == "__main__":
    serve(TransLogger(app, setup_console_handler=False), host="0.0.0.0", port=8000)
    pass