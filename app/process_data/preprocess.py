import os, sys
sys.path.append(os.path.abspath('.'))
from utils.log_util import logger
import re
import random
from pathlib import Path
import json
import pandas as pd
import numpy as np
from pandas import DataFrame
from icecream import ic
ic.configureOutput(includeContext=True, argToStringFunction=lambda _: str(_))


root_input_dir = Path('/mnt/sdc/af_input')
pos_complex_in_one_seq_dir = root_input_dir / 'pos_complex_in_one_seq'
pos_dir = root_input_dir / 'pos'


def create_pos_complex_in_one_seq():
    """  """
    for file in pos_dir.glob('*.fasta'):
        out_file = pos_complex_in_one_seq_dir / file.name
        header = file.stem
        seqs = []
        for line in file.read_text().splitlines():
            if line.startswith('>'): continue
            seqs.append(line.strip())
        seq = ':'.join(seqs)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(f'>{header}\n{seq}\n')


if __name__ == "__main__":
    create_pos_complex_in_one_seq()
    pass            
