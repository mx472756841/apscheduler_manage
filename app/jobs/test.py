import datetime

from flask_apscheduler.scheduler import LOGGER


def test_job():
    """
    测试job
    """
    LOGGER.info(f"test_job >>>>> {datetime.datetime.now()}")
