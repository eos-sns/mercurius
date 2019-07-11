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

    def __str__(self):
        out = "*** data: {}\n".format(self.data)
        out += "*** form: {}\n".format(self.form)
        return out
