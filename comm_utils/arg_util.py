import argparse
import logging
from datetime import datetime
from pathlib import Path

DATE_TIME = "%Y_%m_%d %H:%M:%S"


def save_args(args, output_dir='.', with_time_at_filename=False):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    t0 = datetime.now().strftime(DATE_TIME)
    if with_time_at_filename:
        out_file = output_dir / f"args-{t0}.txt"
    else:
        out_file = output_dir / f"args.txt"
    with open(out_file, "w", encoding='utf-8') as f:
        f.write(f'{t0}\n')
        for arg, value in vars(args).items():
            f.write(f"{arg}: {value}\n")


def log_args(args, logger=None, save_dir=None):
    if logger is None:
        logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO,
            format='%(asctime)s %(filename)s %(lineno)d: %(message)s',
            datefmt='%y-%m-%d %H:%M')

    for arg, value in vars(args).items():
        logger.info(f"{arg}: {value}")

    if save_dir is not None:
        logger.info('Save args to the dir %s', save_dir)
        save_args(args, save_dir)