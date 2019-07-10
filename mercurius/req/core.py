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
        self.input_file, self.error_file = None, None
        self.form = req.form
        self.meta_data = None
        self.upload_folder = None
