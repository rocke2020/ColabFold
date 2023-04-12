import os, sys
from app.colabFold_batch_runner import main
from utils.log_util import logger


if __name__ == "__main__":
    main()
    logger.info('end')
    pass