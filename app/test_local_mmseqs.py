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


logger = get_logger(name=__name__, log_file=Path(__file__).with_suffix('.log'), log_level=logging.INFO)


host_url = 'http://127.0.0.1:8888'
submission_endpoint = 'ticket/msa'
query = '>101\nVNPTVFFDIAVDGEPLGRVSFELFADKVPKTAENFRALSTGEKGFGYKGSCFHRIIPGFMCQGGDFTRHNGTGGKSIYGEKFEDENFILKHTGPGILSMANAGPNTNGSQFFICTAKTEWLDGKHVVFGKVKEGMNIVEAMERFGSRNGKTSKKITIADCGQLE\n>102\nHAGPIA\n'
mode = 'env'
try:
    res = requests.post(f'{host_url}/{submission_endpoint}', data={'q':query,'mode': mode}, timeout=6.02)
    out = res.json()
    logger.info('%s', out)
except Exception as identifier:
    logger.exception(f'query {query}', exc_info=identifier)
    raise identifier
