import os, sys
import re
import random
from pathlib import Path
import hashlib


def calculate_file_md5(filename):
    """ For small file """
    with open(filename,"rb") as f:
        bytes = f.read()
        readable_hash = hashlib.md5(bytes).hexdigest()
        return readable_hash


def compare_file_md5_with_af_params():
    """ all the same for .npz files from cf to af """
    af_params_dir = Path('/mnt/sdc/af_data/params')
    all_af_params_files = [file.stem for file in af_params_dir.glob('*.npz')]
    cf_parmas_dir = Path('/mnt/sdc/cf_params')
    for file in cf_parmas_dir.glob('*.npz'):
        print(file.name)
        if file.stem in all_af_params_files:
            af_file = af_params_dir / file.name
            af_md5 = calculate_file_md5(af_file)
            cf_md5 = calculate_file_md5(file)
            if af_md5 != cf_md5:
                print(f'{file} is diff between af and cf')
        else:
            print(f'{file} is not in af')


compare_file_md5_with_af_params()