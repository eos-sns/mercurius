# !/usr/bin/python3
# coding: utf-8

# Copyright 2019 Stefano Fogarollo


""" Install dependencies """

from setuptools import setup, find_packages

LITTLE_DESCRIPTION = "Middleware to handle user requests and forward them to helios"

DESCRIPTION = \
    "mercurius\n\n" + LITTLE_DESCRIPTION + "\n\
    Install\n\n\
    - $ pip install .\n\
    \n\
    Questions and issues\n\n\
    The Github issue tracker is only for bug reports and feature requests."

setup(
    name="mercurius",
    version="1.0",
    description=LITTLE_DESCRIPTION,
    long_description=DESCRIPTION,
    license="MIT",
    keywords="eos flask middleware",
    url="https://github.com/eos-sns/mercurius",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "werkzeug",
        "flask",
        "helios", 'httplib2', 'google-api-python-client'
    ],
    entry_points={
        "console_scripts": ["mercurius = mercurius.server:cli"]
    }
)
