# !/usr/bin/python3
# coding: utf-8


""" Models and data structure """


class XMLHttpRequest:
    """ Parse XMLHttpRequest """

    def __init__(self, req):
        """
        :param req: Request
            Client request
        """

        self.data = req.data
        self.form = req.form

    def get_params(self):
        return self.data['params']

    def get_files(self):
        return self.data['files']

    def get_user(self):
        return self.data['user']

    def __str__(self):
        out = "*** data: {}\n".format(self.data)
        out += "*** form: {}\n".format(self.form)
        return out

    def get_status(self):
        must_be_keys = ['params', 'files', 'user']
        for key in must_be_keys:
            if key not in self.data:
                return False

        return True
