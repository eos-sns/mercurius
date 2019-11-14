# !/usr/bin/python3
# coding: utf-8

import os
import traceback  # todo debug only
from multiprocessing.pool import ThreadPool

from flask import jsonify
from helios.config.configuration import EosConfiguration
from helios.helios.core import Helios
from helios.helios.h5 import MongoH5Collection

from mercurius.emails.mailer import notify_user_of_good_request, notify_user_of_download
from mercurius.req.core import PostRequest, PutRequest

ROOT_FOLDER = os.getenv('MERCURIUS_FOLDER')
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
    0: ['21cm_lightcone', '21cm_lightcone_z'],  # lightcone
    1: ['density_lightcone', '21cm_lightcone_z'],  # density lightcone
    2: ['LF_UV_z', 'M_UV_z', 'M_h_z'],  # luminosity function
    3: ['Tb_global', 'redshifts_global'],  # global signal
    4: ['neutral_fraction_global', 'redshifts_global'],  # neutral fraction global
    5: ['co-eval_PS_z', 'cp-eval_k', 'co-eval_PS_error_z'],  # co-eval PS
    6: ['lightcone_PS_z', 'lightcone_k', 'lightcone_PS_error_z']  # lightcone PS
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
AVERAGE_FILE_SIZE_MB = 5
AVERAGE_COMPRESSION_RATIO = 0.25


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
            out += USER_FILES2MONGO[i]

    out = list(set(out))  # some fields may be in more than 1 key

    return out


def handle_db_results(helios, results, files_to_get):
    if results:
        h5s = MongoH5Collection(results, helios.config.get_tmp())
        output_path = h5s.save_to_disk(helios.config.get_output()["folder"], files_to_get)
        download_link = helios.get_download_link(output_path)
        return download_link

    return None


def handle_query(user, params, files_requested):
    helios = Helios(MERCURIUS_CONFIGURATION)
    params = convert_user_dict(params)
    query = helios.builder().from_dict(params).build()
    files_to_get = convert_user_files(files_requested)
    results = query.execute()
    download_link = handle_db_results(helios, results.get(), files_to_get)
    download_info = {
        'timeout': 'in 14 days',
        'link': download_link
    }
    notify_user_of_download(user['email'], user['name'], download_info)


def estimate_query_time(params, files_requested):
    helios = Helios(MERCURIUS_CONFIGURATION)
    params = convert_user_dict(params)
    query = helios.builder().from_dict(params).build()
    n_files = len(convert_user_files(files_requested))
    n_results = query.count()
    tot_size = n_results * n_files * AVERAGE_FILE_SIZE_MB
    compressed_size = tot_size * AVERAGE_COMPRESSION_RATIO
    return {
        'nSimulations': n_results,
        'mbSize': compressed_size,
    }


def return_bad_request(_):
    return jsonify(**BAD_REQ)


# todo decorator to handle exception, input error
def handle_post_request(req):
    xhr = PostRequest(req)
    if xhr.is_ok():
        user, params, files = xhr.get_user(), xhr.get_params(), xhr.get_files()

        try:
            pool = ThreadPool(processes=1)

            res = pool.apply_async(estimate_query_time, (params, files))  # thread
            eta = res.get()  # wait until thread returns
            notify_user_of_good_request(user['email'], user['name'], eta)
            pool.apply_async(handle_query(user, params, files))  # thread

            return jsonify(**GOOD_REQ)
        except Exception:
            traceback.print_exc()  # todo debug only
            return jsonify(**GOOD_INPUT_BAD_HANDLE_REQ)

    return jsonify(**BAD_REQ)


def handle_put_request(req):
    xhr = PutRequest(req)
    if xhr.is_ok():
        params, files = xhr.get_params(), xhr.get_files()

        try:
            result = estimate_query_time(params, files)
            return jsonify(**result)
        except Exception:
            traceback.print_exc()  # todo debug only
            return jsonify(**GOOD_INPUT_BAD_HANDLE_REQ)

    return jsonify(**BAD_REQ)
