# coding: utf-8

import logging

# логгер для всего пакета
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

from .utils import *
from .path import *
from .templates import *
from .settings import *
from .operations import *
