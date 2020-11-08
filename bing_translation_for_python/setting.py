from configparser import ConfigParser, NoSectionError
from random import randint
from .public import errors
from typing import Dict
import os

BASE_DIR_INSIDE = os.path.dirname(os.path.abspath(__file__))
BASE_DIR_OUTSIDE = os.path.dirname(BASE_DIR_INSIDE)


CONF_PATH = os.path.join(BASE_DIR_OUTSIDE, 'ini/conf.ini')

LANGUAGE_CODE_PATH = os.path.join(BASE_DIR_OUTSIDE, 'ini/language_code.ini')

SEMANTIC_URL = 'https://cn.bing.com/tlookupv3'
HOME_PAGE_URL = 'https://cn.bing.com/translator/'
TRANSLATOR_ENGINE_URL = 'https://cn.bing.com/ttranslatev3'

AGENTS = [
    'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
    'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
]
HEADERS = {'User-Agent': AGENTS[randint(0, len(AGENTS) - 1)]}


def file_check(func):
    def run(path, *argv, **kwargs):
        if os.access(path, os.F_OK) and os.access(path, os.R_OK):
            return func(path, *argv, **kwargs)
        raise errors.FileError(
            F'没有找到配置文件，或文件不可访问： \n{path}'
        )

    return run


class Conf:

    def __init__(self):
        self.__conf__ = self.read_inf(CONF_PATH)

    @staticmethod
    @file_check
    def read_inf(path: str) -> Dict[str, Dict[str, str]]:
        """读取配置文件"""
        c_p = ConfigParser()
        c_p.read(path, encoding='UTF-8')

        return {i: dict(c_p.items(i)) for i in c_p.sections()}

    @staticmethod
    def save_ini(path: str, data_table: Dict[str, Dict[str, str]]):
        c_p = ConfigParser()
        c_p.read(path, encoding='UTF-8')

        for section in data_table.keys():
            for option in data_table[section].keys():
                try:
                    c_p.set(section, option, data_table[section][option])
                except NoSectionError:
                    c_p.add_section(section)
                    c_p.set(section, option, data_table[section][option])

        with open(path, 'w', encoding='UTF-8') as file:
            c_p.write(file)

    def template_of_translator(self, fromlang, tolang, text) -> dict:
        return {
            'url': TRANSLATOR_ENGINE_URL,
            'headers': HEADERS,
            # TODO 待移除参数
            # 'params': self.__conf__['params'],
            'data': {
                'fromLang': fromlang,
                'to': tolang,
                'text': text,
            }
        }

    def template_of_semantic(self, fromlang, tolang, text):
        return {
            'url': SEMANTIC_URL,
            'headers': HEADERS,
            # TODO 待移除参数
            # 'params': self.__conf__['params'],
            'data': {
                'from': fromlang,
                'to': tolang,
                'text': text,
            }
        }
