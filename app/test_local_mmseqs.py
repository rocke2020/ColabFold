import os, sys
import re
import random
from pathlib import Path
import json
import logging
import requests
sys.path.append(os.path.abspath('.'))
from utils.log_util import get_logger
import logging
from requests import get, post
from time import sleep, time
from icecream import ic
ic.configureOutput(includeContext=True, argToStringFunction=lambda _: str(_))


logger = get_logger(name=__name__, log_file=Path(__file__).with_suffix('.log'), log_level=logging.INFO)

use_online_url = 1
if use_online_url:
    host_url = "https://api.colabfold.com"
else:
    host_url = 'http://127.0.0.1:8888'



def test_msa():
    """  """
    
    query = '>101\nVNPTVFFDIAVDGEPLGRVSFELFADKVPKTAENFRALSTGEKGFGYKGSCFHRIIPGFMCQGGDFTRHNGTGGKSIYGEKFEDENFILKHTGPGILSMANAGPNTNGSQFFICTAKTEWLDGKHVVFGKVKEGMNIVEAMERFGSRNGKTSKKITIADCGQLE\n>102\nHAGPIA\n'
    mode = 'env'
    submission_endpoint = 'ticket/msa'
    try:
        res = requests.post(f'{host_url}/{submission_endpoint}', data={'q':query,'mode': mode}, timeout=6.02)
        out = res.json()
        logger.info('%s', out)
    except Exception as identifier:
        logger.exception(f'query {query}', exc_info=identifier)
        raise identifier


def test_pairing():
    """  """
    
    query = '>101\nVNPTVFFDIAVDGEPLGRVSFELFADKVPKTAENFRALSTGEKGFGYKGSCFHRIIPGFMCQGGDFTRHNGTGGKSIYGEKFEDENFILKHTGPGILSMANAGPNTNGSQFFICTAKTEWLDGKHVVFGKVKEGMNIVEAMERFGSRNGKTSKKITIADCGQLE\n>102\nHAGPIA\n'
    mode = ''
    submission_endpoint = 'ticket/pair'
    try:
        res = requests.post(f'{host_url}/{submission_endpoint}', data={'q':query,'mode': mode}, timeout=6.02)
        out = res.json()
        logger.info('%s', out)
    except Exception as identifier:
        logger.exception(f'query {query}', exc_info=identifier)
        raise identifier

ID = '067a-BpkfSS3NmHh8alM6OB9VCkHbdbUZEK_XQ'


def check_status(id='067a-BpkfSS3NmHh8alM6OB9VCkHbdbUZEK_XQ'):
    """  """
    out = status(id)
    ic(out['status'])


def status(ID):
    while True:
        error_count = 0
        try:
            res = requests.get(f'{host_url}/ticket/{ID}', timeout=6.02)
        except requests.exceptions.Timeout:
            logger.warning("Timeout while fetching status from MSA server. Retrying...")
            continue
        except Exception as e:
            error_count += 1
            logger.warning(f"Error while fetching result from MSA server. Retrying... ({error_count}/5)")
            logger.warning(f"Error: {e}")
            time.sleep(5)
            if error_count > 5:
                raise
            continue
        break
    try:
        out = res.json()
    except ValueError:
        logger.error(f"Server didn't reply with json: {res.text}")
        out = {"status":"ERROR"}
    return out
    

def download(ID, path):
    error_count = 0
    while True:
        try:
            res = requests.get(f'{host_url}/result/download/{ID}', timeout=6.02)
        except requests.exceptions.Timeout:
            logger.warning("Timeout while fetching result from MSA server. Retrying...")
            continue
        except Exception as e:
            error_count += 1
            logger.warning(f"Error while fetching result from MSA server. Retrying... ({error_count}/5)")
            logger.warning(f"Error: {e}")
            time.sleep(5)
            if error_count > 5:
                raise
            continue
        break
    with open(path,"wb") as out: out.write(res.content)


# test_msa()
test_pairing()
# check_status()
# download(ID, 'out.tar.gz')