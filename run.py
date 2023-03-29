import os, sys
from app.AlphaFold2_batch import main
from utils.log_util import logger


if __name__ == "__main__":
    main()
    logger.info('end')
    pass