import json
import logging
import math
import os
import random
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
from icecream import ic

ic.configureOutput(includeContext=True, argToStringFunction=str)
ic.lineWrapWidth = 120
sys.path.append(os.path.abspath('.'))

SEED = 0
random.seed(SEED)
np.random.seed(SEED)
cf_out_dir = Path('/mnt/nas/alphafold/af_out/cf_FGF5-all-pos2')


def collect_failed_process():
    """  
    ('CNGNTC', '2023-11-14 21:40:54'), ('CNGTNC', '2023-11-15 00:01:08'), ('CNNNTC', '2023-11-15 02:49:15'), ('CNNTNC', '2023-11-15 05:06:01'), ('CNNTTC', '2023-11-15 07:13:50'), ('CNTGNC', '2023-11-15 11:21:06'), ('CNTGTC', '2023-11-15 13:28:50'), ('CNTNTC', '2023-11-15 16:02:36'), ('CNTTNC', '2023-11-15 19:15:18'), ('AMCYMACYM', '2023-11-16 13:53:57')
    """
    failed_sequences = []
    for out_path in cf_out_dir.iterdir():
        if not out_path.is_dir():
            continue
        is_finished = False
        for file in out_path.iterdir():
            if file.name.endswith('.done.txt'):
                is_finished = True
                break
        if not is_finished:
            mtime = datetime.fromtimestamp(out_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            failed_sequences.append((out_path.stem, mtime))
    failed_sequences = sorted(failed_sequences, key=lambda x: x[1])
    ic(len(failed_sequences))
    ic(failed_sequences)


if __name__ == '__main__':
    collect_failed_process()
