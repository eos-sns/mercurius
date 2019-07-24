# !/usr/bin/python3
# coding: utf-8

from flask import Flask, request

from mercurius.config import APP_NAME, APP_HOST, APP_PORT
from mercurius.req.handlers import handle_request

app = Flask(APP_NAME)


@app.route("/", methods=["POST"])
def index():
    response = handle_request(request)
    return response


if __name__ == "__main__":
    app.debug = True

    app.run(host=APP_HOST, port=APP_PORT, debug=True, threaded=True)
