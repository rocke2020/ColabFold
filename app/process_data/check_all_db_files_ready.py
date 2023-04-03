import os, sys
import re
import random
from pathlib import Path
import json
import pandas as pd
import numpy as np
from pandas import DataFrame


db_root = Path('/mnt/sdc/colabfold_db')
ready_files = [
    'UNIREF30_READY',
    'COLABDB_READY',
    'PDB_READY',
    'PDB70_READY',
    'PDB_MMCIF_READY',
]

db_files = [file.name for file in db_root.iterdir()]
for file in ready_files:
    if file not in db_files:
        print(f'{file} not exist')
    else:
        print(f'{file} exist')