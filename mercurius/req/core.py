# !/usr/bin/python3
# coding: utf-8


""" Models and data structure """

import json


class XMLHttpRequest:
    """ Parse XMLHttpRequest """

    def __init__(self, req):
        """
        :param req: Request
            Client request
        """

        self.data = json.loads(req.data)
        self.form = req.form.to_dict(flat=False)

    def get_params(self):
        return self.data['params']

    def get_files(self):
        return self.data['files']

    def get_user(self):
        return self.data['user']

    def __str__(self):
        out = "- Data: {}\n".format(self.data)
        out += "- Form: {}\n".format(self.form)
        return out

    def get_status(self):
        must_be_keys = ['params', 'files', 'user']
        for key in must_be_keys:
            if key not in self.data:
                return False

        return True
