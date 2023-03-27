import json
import dataclasses
from decimal import Decimal
import dataclasses, json
from typing import Tuple, List
import numpy
import math
import hashlib
import socket
import os, sys
sys.path.append(os.path.abspath('.'))
from utils.log_util import logger
from pathlib import Path
import shutil
import re


class FileUtil(object):
    """
    文件工具类
    """
    @classmethod
    def read_raw_text(cls, file_path) ->List[str]:
        """
        读取原始文本数据，每行均为纯文本
        """
        all_raw_text_list = []
        with open(file_path, "r", encoding="utf-8") as raw_text_file:
            for item in raw_text_file:
                item = item.strip()
                all_raw_text_list.append(item)

        return all_raw_text_list

    @classmethod
    def write_raw_text(cls, texts, file_path):
        """
        写入文本数据，每行均为纯文本
        """
        with open(file_path, "w", encoding="utf-8") as f:
            for item in texts:
                f.write(f'{item}\n')

    @classmethod
    def read_json(cls, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @classmethod
    def write_json(cls, data, file_path, ensure_ascii=False):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=ensure_ascii, indent=4, cls=JSONEncoder)


def dataclass_from_dict(klass, dikt):
    try:
        fieldtypes = klass.__annotations__
        return klass(**{f: dataclass_from_dict(fieldtypes[f], dikt[f]) for f in dikt})
    except AttributeError:
        # Must to support List[dataclass]
        if isinstance(dikt, (tuple, list)):
            return [dataclass_from_dict(klass.__args__[0], f) for f in dikt]
        return dikt


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, (Tuple, set)):
            return list(o)
        if isinstance(o, bytes):
            return o.decode()
        if isinstance(o, numpy.ndarray):
            return o.tolist()
        return super().default(o)


def get_partial_files(input_files, total_parts_num=-1, part_num=-1, start_index=-1) ->List:
    """ part_seq starts from 1.
        If set start_index > 0, directly get partial input_files[start_index:]
    """
    if start_index > 0:
        partial_files = input_files[start_index:]
    elif part_num > 0 and total_parts_num > 0:
        input_files_num = len(input_files)
        num_per_part = math.ceil(input_files_num / total_parts_num)
        start_i = (part_num - 1) * num_per_part
        end_i = part_num * num_per_part
        partial_files = input_files[start_i: end_i]
    else:
        partial_files = input_files
    return partial_files


def calculate_file_md5(filename):
    """ For small file """
    with open(filename,"rb") as f:
        bytes = f.read()
        readable_hash = hashlib.md5(bytes).hexdigest()
        return readable_hash


def compare_files_between_2_folders(dir1: Path, dir2: Path):
    """ check files in dir1 are whether all the same as that in dir2, note the dir1/dir2 sequence! """
    files2 = [file.name for file in dir2.iterdir()]
    all_same = True
    for file in dir1.iterdir():
        if file.name not in files2:
            logger.info('%s not in dir2 %s', file, dir2)
            all_same = False
        else:
            file_md5 = calculate_file_md5(file)
            file2_md5 = calculate_file_md5((dir2 / file.name))
            if file_md5 != file2_md5:
                logger.info('%s are diff between the 2 dir', file)
                all_same = False
    if all_same:
        logger.info('files in %s are all the same as that in %s', dir1, dir2)


def calculate_file_md5_large_file(filename):
    """ For large file to read by chunks in iteration. """
    md5_hash = hashlib.md5()
    with open(filename,"rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()


def get_local_ip(only_last_address=True):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        local_ip = s.getsockname()[0]
        logger.info('local ip: %s', local_ip)
    except Exception as identifier:
        logger.info('cannot get ip with error %s\nSo the local ip is 127.0.0.1', identifier)
        local_ip = '127.0.0.1'
    finally:
        s.close()
    if only_last_address:
        local_ip = local_ip.split('.')[-1]
    logger.info('local_ip %s', local_ip)
    return local_ip


def del_file_dir(filename_starts='6roy_A_C', folders=None):
    """  """
    if not folders:
        folders = [
            Path('/mnt/sdc/af_input/pos_pse_files'),
            Path('/mnt/sdc/af_input/pos'),
            Path('/mnt/sdc/af_out/pos'),
            Path('/mnt/sdc/af_out_simple'),
        ]
    for folder in folders:
        for file in folder.iterdir():
            if file.stem.startswith(filename_starts):
                if file.is_dir():
                    shutil.rmtree(file)
                else:
                    file.unlink()

def clean_line_prefix_in_log_file(log_dir):
    """  """
    date_prefix = re.compile(f'^\d+-\d+(-\d+)? \d+:\d+:\d+ [\w_.]+ \d+: ')

    for file in Path(log_dir).glob('*.log'):
        lines = []
        logger.info('%s', file)
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                _line = re.sub(date_prefix, '', line)
                lines.append(_line)
        with open(file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line)

if __name__ == "__main__":
    # del_file_dir()
    clean_line_prefix_in_log_file('app/postprocess/data')
    pass