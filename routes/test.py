from flask import Blueprint


test = Blueprint("test", __name__)


@test.route("/")
def main():
    return "test"