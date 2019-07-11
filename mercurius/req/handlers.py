# !/usr/bin/python3
# coding: utf-8

from flask import jsonify

from mercurius.req.core import XMLHttpRequest


def handle_request(req):
    xhr = XMLHttpRequest(req)
    print('handling req', xhr)

    response = jsonify(
        status="wow"
    )
    return response
