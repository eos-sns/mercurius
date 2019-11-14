# !/usr/bin/bash
# -*- coding: utf-8 -*-

export MERCURIUS_FOLDER=/opt/eos/mercurius

echo "I am in" $(pwd)

source ${MERCURIUS_FOLDER}/venv/bin/activate
echo "virtualenv is ON"

python ${MERCURIUS_FOLDER}/mercurius/server.py
