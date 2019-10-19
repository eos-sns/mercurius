# !/usr/bin/python3
# coding: utf-8


""" Models and data structure """

import abc
import json


class HttpRequest:
    """ Parse XMLHttpRequest """

    def __init__(self, req):
        """
        :param req: Request
            Client request
        """

        self.data = json.loads(req.data)
        self.form = req.form.to_dict(flat=False)

    def get_key(self, key):
        return self.data[key]

    def check_keys(self, must_be_keys):
        for key in must_be_keys:
            if key not in self.data:
                return False

        return True

    def __str__(self):
        out = "- Data: {}\n".format(self.data)
        out += "- Form: {}\n".format(self.form)
        return out

    @abc.abstractmethod
    def get_params(self):
        return {}

    @abc.abstractmethod
    def is_ok(self):
        return False


class PostRequest(HttpRequest):
    def get_params(self):
        return self.data['params']

    def get_files(self):
        return self.data['files']

    def get_user(self):
        return self.data['user']

    def is_ok(self):
        return self.check_keys(['params', 'files', 'user'])


class PutRequest(HttpRequest):
    def get_params(self):
        return self.data['params']

    def get_files(self):
        return self.data['files']

    def is_ok(self):
        return self.check_keys(['params', 'files'])
