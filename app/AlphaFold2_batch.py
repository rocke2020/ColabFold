import os, sys
import re, random
from pathlib import Path
import json
import pandas as pd
import numpy as np
from pandas import DataFrame
from utils.log_util import logger
from icecream import ic
ic.configureOutput(includeContext=True, argToStringFunction=lambda _: str(_))
from sys import version_info
python_version = f"{version_info.major}.{version_info.minor}"
logger.info('python_version %s', python_version)
from colabfold.batch import get_queries, run
from colabfold.utils import setup_logging


root_input_dir = Path('/mnt/sdc/af_input/pos_complex_in_one_seq')
test_file = '1awr_C_I.fasta'
default_data_dir = Path('/mnt/sdc/af_data')
msa_mode = "MMseqs2 (UniRef+Environmental)" #@param ["MMseqs2 (UniRef+Environmental)", "MMseqs2 (UniRef only)","single_sequence","custom"]
num_models = 5 #@param [1,2,3,4,5] {type:"raw"}
num_recycles = 9 #@param [1,3,6,12,24,48] {type:"raw"}
stop_at_score = 100 #@param {type:"string"}
#@markdown - early stop computing models once score > threshold (avg. plddt for "structures" and ptmscore for "complexes")
use_custom_msa = False
use_amber = True #@param {type:"boolean"}
use_templates = True #@param {type:"boolean"}
do_not_overwrite_results = False #@param {type:"boolean"}
zip_results = False #@param {type:"boolean"}


single_file_input = 0
if single_file_input:
    input_dir = root_input_dir / test_file
else:
    input_dir = root_input_dir
result_dir = f'app/af_out/{Path(input_dir).stem}' #@param {type:"string"}
Path(result_dir).mkdir(exist_ok=1, parents=1)
if 'logging_setup' not in globals():
    setup_logging(Path(result_dir).joinpath("log.txt"))
    logging_setup = True


def main():
    """  """
    queries, is_complex = get_queries(input_dir)
    run(
        queries=queries,
        result_dir=result_dir,
        use_templates=use_templates,
        use_amber=use_amber,
        msa_mode=msa_mode,
        model_type="auto",
        num_models=num_models,
        num_recycles=num_recycles,
        model_order=[1, 2, 3, 4, 5],
        is_complex=is_complex,
        data_dir=default_data_dir,
        keep_existing_results=do_not_overwrite_results,
        rank_by="auto",
        pair_mode="unpaired+paired",
        stop_at_score=stop_at_score,
        zip_results=zip_results,
        num_seeds=5,
        num_relax=5,
    )