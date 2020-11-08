import os

BASE_DIR_INSIDE = os.path.dirname(os.path.abspath(__file__))
BASE_DIR_OUTSIDE = os.path.dirname(BASE_DIR_INSIDE)


CONF_PATH = os.path.join(BASE_DIR_OUTSIDE, 'ini/conf.ini')

LANGUAGE_CODE_PATH = os.path.join(BASE_DIR_OUTSIDE, 'ini/language_code.ini')
