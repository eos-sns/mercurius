# !/usr/bin/python3
# coding: utf-8

import os
from multiprocessing.pool import ThreadPool

from flask import jsonify
from helios.config.configuration import EosConfiguration
from helios.helios.core import Helios
from helios.helios.h5 import MongoH5Collection

from mercurius.emails.mailer import notify_user_of_good_request, notify_user_of_download
from mercurius.req.core import XMLHttpRequest

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(HERE)))
DEFAULT_CONFIG_FOLDER = os.path.join(ROOT_FOLDER, 'config')
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_FOLDER, 'config.json')
MERCURIUS_CONFIGURATION = EosConfiguration(DEFAULT_CONFIG_FILE)
USER_PARAMS2MONGO = {
    'alphaEsc': 'ALPHA_ESC',
    'alphaStar': 'ALPHA_STAR',
    'fEsc10': 'F_ESC10',
    'fStar10': 'F_STAR10',
    'lX': 'L_X',
    'mTurn': 'M_TURN',
    'tStar': 't_STAR',
    'sigma8': 'SIGMA_8',
    'xRaySpecIndex': 'X_RAY_SPEC_INDEX'
}  # convert frontend params 2 mongodb keys
USER_FILES2MONGO = {
    0: 'co-eval_k',
    1: 'co-eval_PS_z'
}
GOOD_REQ = {
    'status': 'Done!',
    'code': '200'
}
GOOD_INPUT_BAD_HANDLE_REQ = {
    'status': 'Cannot handle request!',
    'code': '800'
}
BAD_REQ = {
    'status': 'Cannot parse request!',
    'code': '300'
}


def convert_user_dict(d):
    out = {}

    for key, val in d.items():
        new_key = USER_PARAMS2MONGO[key]
        out[new_key] = val

    return out


def convert_user_files(files):
    out = []

    for i, boolean in enumerate(files):
        if boolean:
            out.append(USER_FILES2MONGO[i])

    return out


def handle_db_results(helios, results):
    if results:
        h5s = MongoH5Collection(results, helios.config.get_tmp())
        output_path = h5s.save_to_disk(helios.config.get_output()["folder"])
        download_link = helios.get_download_link(output_path)
        return download_link

    return None


def handle_query(user, params, files_requested):
    helios = Helios(MERCURIUS_CONFIGURATION)
    params = convert_user_dict(params)
    query = helios.builder() \
        .from_dict(params) \
        .build()

    files_to_get = convert_user_files(files_requested)  # todo filter for files requested
    results = query.execute()
    download_link = handle_db_results(helios, results.get())
    download_info = {
        'timeout': 'in 14 days',
        'link': download_link
    }
    notify_user_of_download(user['email'], user['name'], download_info)


def estimate_query_time(params, files_requested):
    # todo estimate time based on how big are the ranges of each param in params
    return {
        'long time': 'in a few hours'
    }


def handle_request(req):
    xhr = XMLHttpRequest(req)
    is_ok = xhr.get_status()

    if is_ok:
        user, params, files = xhr.get_user(), xhr.get_params(), xhr.get_files()

        try:
            pool = ThreadPool(processes=1)

            res = pool.apply_async(estimate_query_time, (params, files))  # thread
            eta = res.get()  # wait until thread returns
            notify_user_of_good_request(user['email'], user['name'], eta)

            pool.apply_async(handle_query(xhr.get_user(), xhr.get_params(), xhr.get_files()))  # thread

            return jsonify(**GOOD_REQ)
        except Exception as e:
            return jsonify(**GOOD_INPUT_BAD_HANDLE_REQ)

    return jsonify(**BAD_REQ)
