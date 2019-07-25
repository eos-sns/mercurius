from helios.config.configuration import EosConfiguration
from helios.helios.core import Helios
from helios.helios.h5 import MongoH5Collection
from helios.logs.logger import Logger

MERCURIUS_CONFIGURATION = EosConfiguration('/home/stefano/Work/sns/eos/mercurius/config/config.json')


def handle_db_results(helios, results):
    if results:
        h5s = MongoH5Collection(results, helios.config.get_tmp())
        output_path = h5s.save_to_disk(helios.config.get_output()["folder"])
        download_link = helios.get_download_link(output_path)
        return download_link

    return None


def woow():
    helios = Helios(MERCURIUS_CONFIGURATION)
    results = [{
        "_id": "5d2ed40f8562183e302a2681",
        "ALPHA_ESC": -0.5,
        "ALPHA_STAR": 0.5,
        "ALPHA_UVB": 5.0,
        "BOX_LEN": 300.0,
        "CLUMPING_FACTOR": 2.0,
        "CRIT_DENS_TRANSITION": 1.5,
        "DELTA_R_HII_FACTOR": 1.10000002384186,
        "DIM": 200.0,
        "EVOLVE_DENSITY_LINEARLY": 0.0,
        "FILTER": 0.0,
        "FIND_BUBBLE_ALGORITHM": 2.0,
        "F_ESC10": -1.30102999566,
        "F_STAR10": -1.0,
        "HEAT_FILTER": 0.0,
        "HII_DIM": 50.0,
        "HII_EFF_FACTOR": 30.0,
        "HII_FILTER": 1.0,
        "HII_ROUND_ERR": 9.99999974737875e-06,
        "HMF": 1.0,
        "INHOMO_RECO": 1.0,
        "INITIAL_REDSHIFT": 300.0,
        "ION_Tvir_MIN": 4.69897,
        "L_X": 40.5,
        "MAX_DVDR": 0.200000002980232,
        "MIN_DENSITY_LOW_LIMIT": 9.0000000341206e-08,
        "M_MIN_in_Mass": 1.0,
        "M_TURN": 8.7,
        "M_WDM": 2.0,
        "NBINS_LF": 100.0,
        "NUM_FILTER_STEPS_FOR_Ts": 40.0,
        "NU_X_BAND_MAX": 2000.0,
        "NU_X_MAX": 10000.0,
        "NU_X_THRESH": 500.0,
        "N_POISSON": 5.0,
        "N_RSD_STEPS": 20.0,
        "OMb": 0.0486,
        "OMk": 0.0,
        "OMl": 0.6925,
        "OMm": 0.3075,
        "OMn": 0.0,
        "OMr": 8.60000000102445e-05,
        "OMtot": 1.0,
        "PHOTON_CONS": 1.0,
        "POWER_INDEX": 0.97,
        "POWER_SPECTRUM": 0.0,
        "P_CUTOFF": 0.0,
        "PhotonConsEnd": 0.25,
        "PhotonConsStart": 0.995000004768372,
        "Pop": 2.0,
        "Pop2_ion": 5000.0,
        "Pop3_ion": 44021.0,
        "R_BUBBLE_MAX": 50.0,
        "R_XLy_MAX": 500.0,
        "R_smooth_density": 0.200000002980232,
        "RecombPhotonCons": 0.0,
        "SECOND_ORDER_LPT_CORRECTIONS": 1.0,
        "SHETH_b": 0.150000005960464,
        "SHETH_c": 0.0500000007450581,
        "SIGMA_8": 0.82,
        "SMOOTH_EVOLVED_DENSITY_FIELD": 0.0,
        "SUBCELL_RSD": 1.0,
        "TK_at_Z_HEAT_MAX": -1.0,
        "T_USE_VELOCITIES": 1.0,
        "USE_FFTW_WISDOM": 1.0,
        "USE_MASS_DEPENDENT_ZETA": 1.0,
        "USE_TS_FLUCT": 1.0,
        "XION_at_Z_HEAT_MAX": -1.0,
        "X_RAY_SPEC_INDEX": 1.0,
        "X_RAY_Tvir_MIN": 4.69897,
        "Y_He": 0.245000004768372,
        "ZPRIME_STEP_FACTOR": 1.01999998092651,
        "Z_HEAT_MAX": 35.0,
        "Zreion_HeII": 3.0,
        "g_x": 1.5,
        "hlittle": 0.6774,
        "n_lc_PS": 11.0,
        "nbins_LF": 100.0,
        "nbins_co-eval_21cmPS": 12.0,
        "nbins_lc_21cmPS": 12.0,
        "random_seed": 42.0,
        "t_STAR": 0.5,
        "tau": 0.0385286808013916,
        "wl": -1.0,
        "path": "/home/stefano/Work/sns/eos/hyperion/_tmp/data_0.h5"
    }]
    download_link = handle_db_results(helios, results)

    logger = Logger('woow')
    logger.log_message('download at {}'.format(download_link))


if __name__ == "__main__":
    woow()
