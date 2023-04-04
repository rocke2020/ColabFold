import os, sys
import re
import random
from pathlib import Path
import json
import logging
import requests
sys.path.append(os.path.abspath('.'))
import logging
from requests import get, post
import time
from icecream import ic
ic.configureOutput(includeContext=True, argToStringFunction=lambda _: str(_))
import logging


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(lineno)d: %(message)s',
                    datefmt='%m-%d %H:%M:%S')


use_online_url = 0
if use_online_url:
    host_url = "https://api.colabfold.com"
else:
    host_url = 'http://127.0.0.1:8888'
logger.info('host_url %s', host_url)


def test_msa_and_pair():
    """  """
    
    query = '>101\nVNPTVFFDIAVDGEPLGRVSFELFADKVPKTAENFRALSTGEKGFGYKGSCFHRIIPGFMCQGGDFTRHNGTGGKSIYGEKFEDENFILKHTGPGILSMANAGPNTNGSQFFICTAKTEWLDGKHVVFGKVKEGMNIVEAMERFGSRNGKTSKKITIADCGQLE\n>102\nHAGPIA\n'
    mode = 'env'
    submission_endpoint = 'ticket/msa'
    res = requests.post(f'{host_url}/{submission_endpoint}', data={'q':query,'mode': mode}, timeout=6.02)
    out = res.json()
    print(out)

    mode = ''
    submission_endpoint = 'ticket/pair'
    res = requests.post(f'{host_url}/{submission_endpoint}', data={'q':query,'mode': mode}, timeout=6.02)
    out = res.json()
    print(out)

import logging
import requests
import time

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s %(lineno)d: %(message)s',
                    datefmt='%m-%d %H:%M:%S')
# host_url = 'http://127.0.0.1:8888'


def test_pairing():
    """  """
    query = '>101\nVNPTVFFDIAVDGEPLGRVSFELFADKVPKTAENFRALSTGEKGFGYKGSCFHRIIPGFMCQGGDFTRHNGTGGKSIYGEKFEDENFILKHTGPGILSMANAGPNTNGSQFFICTAKTEWLDGKHVVFGKVKEGMNIVEAMERFGSRNGKTSKKITIADCGQLE\n>102\nHAGPIA\n'
    mode = ''
    submission_endpoint = 'ticket/pair'
    res = requests.post(f'{host_url}/{submission_endpoint}', data={'q':query,'mode': mode}, timeout=6.02)
    out = res.json()
    logger.info('%s', out)

    # wait for job to finish
    max_seconds = 15000
    ID, TIME = out["id"], 0
    while out["status"] in ["UNKNOWN", "RUNNING", "PENDING", "ERROR"]:
        t = 5 + random.randint(0, 5)
        logger.error(f"Sleeping for {t}s. Reason: {out['status']}")
        time.sleep(t)
        out = status(ID)
        TIME += t
        if TIME > max_seconds and out["status"] != "COMPLETE":
            # something failed on the server side, need to resubmit
            break


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


id_mas = '067a-BpkfSS3NmHh8alM6OB9VCkHbdbUZEK_XQ'
id_pair = '3m6olJuvf_TV0UTKJxnGu3V3YnMxyHkkj915xg'


def check_status(id='067a-BpkfSS3NmHh8alM6OB9VCkHbdbUZEK_XQ'):
    """  """
    out = status(id)
    ic(out['status'])


# test_msa()
test_pairing()
# check_status(id_pair)
# download(ID, 'out.tar.gz')