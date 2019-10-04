# !/usr/bin/bash
# -*- coding: utf-8 -*-

echo "I am in" $(pwd)

source /opt/eos/mercurius/venv/bin/activate
echo "virtualenv is ON"

python /opt/eos/mercurius/mercurius/server.py
