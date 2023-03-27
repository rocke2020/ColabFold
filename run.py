import os, sys
from app.AlphaFold2_batch import main
from utils.log_util import logger


for idx, path in enumerate(sys.path, 1):
    logger.info(f'{idx} - {path}')

if __name__ == "__main__":
    main()
    pass