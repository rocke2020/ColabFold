import logging
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO, datefmt='%y-%m-%d %H:%M',
    format='%(asctime)s %(filename)s %(lineno)d: %(message)s')
import jax


def check_gpu_count():
    """ Returns: 0 means no gpu """
    if jax.default_backend() == 'gpu':
        logger.info('gpu count: %s', jax.local_device_count())
        return jax.local_device_count()
    else:
        logger.warning('no gpu, use CPU!')
        return 0


def get_gpu_device_id(gpu_device_id:str):
    """ if int(gpu_device_id) >= gpu_count: prefer gpu_device_id = '1' """
    gpu_count = check_gpu_count()
    if int(gpu_device_id) >= gpu_count:
        if gpu_count > 1:
            gpu_device_id = '1'
        else:
            gpu_device_id = '0'
    logger.info('gpu_device_id %s', gpu_device_id)
    return gpu_device_id


if __name__ == "__main__":
    get_gpu_device_id('1')
    print(jax.local_devices()[0].platform)
    pass