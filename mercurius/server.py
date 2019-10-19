# !/usr/bin/python3
# coding: utf-8

from flask import Flask, request

from mercurius.config import APP_NAME, APP_HOST, APP_PORT
from mercurius.req.handlers import handle_post_request, handle_put_request, return_bad_request

app = Flask(APP_NAME)


@app.route("/", methods=['PUT', 'POST'])
def index():
    if request.method == 'PUT':
        return handle_put_request(request)
    elif request.method == 'POST':
        return handle_post_request(request)

    return return_bad_request(request)


if __name__ == "__main__":
    app.debug = True
    app.run(host=APP_HOST, port=APP_PORT, debug=True, threaded=True)
