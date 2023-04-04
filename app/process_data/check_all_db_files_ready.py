import os, sys
import re
import random
from pathlib import Path
import json
import pandas as pd
import numpy as np
from pandas import DataFrame


db_root = Path('/mnt/sdc/colabfold_db')
db_file_names = sorted([file.name for file in db_root.iterdir()])
split_idx_pat = re.compile(r'idx(\.\d+)?$')
ready_files = [
    'UNIREF30_READY',
    'COLABDB_READY',
    'PDB_READY',
    'PDB70_READY',
    'PDB_MMCIF_READY',
]


def check_all_db_files_ready():
    """  """
    for file in ready_files:
        if file not in db_file_names:
            print(f'{file} not exist')
        else:
            print(f'{file} exist')


def collect_all_created_index_files():
    """  """
    all_created_index_files = []
    for file in db_file_names:
        if split_idx_pat.search(file):
            all_created_index_files.append(file)
    with open('app/process_data/all_created_index_files.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(all_created_index_files))


collect_all_created_index_files()