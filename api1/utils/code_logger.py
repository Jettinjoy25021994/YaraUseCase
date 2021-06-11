"""
A helper module that sets up a logger

Created By: Jettin Joy
Created On: 06/12/2021
"""

import logging
from logging import config
config.fileConfig('conf/log.conf')
logger = logging.getLogger('extract')
