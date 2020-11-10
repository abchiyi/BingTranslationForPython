from configparser import ConfigParser, NoSectionError
from random import randint

from .public import errors
from pathlib import Path
from typing import Dict
import os

from bs4 import BeautifulSoup as soup
from requests import get

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
    def run(file_name, path, *argv, **kwargs):
        if Path(os.path.join(path, file_name)).is_file():
            return func(file_name, path, *argv, **kwargs)
        raise errors.FileError(
            F'FileNotFound\nPath:\n\t{path}\nFile:\n\t{file_name}'
        )

    return run


def update_language_code():
    response = get(HOME_PAGE_URL)
    bfs = soup(response.text, 'html.parser')
    tags = bfs.find(id='t_tgtAllLang').find_all('option')

    return {tag.attrs['value']: {'text': tag.text} for tag in tags}


class Config:
    def __init__(self, save_path=False, file_name="config.ini"):
        # 验证配置文件模式
        if save_path:
            try:
                self.tgt_lang = self.load(file_name, save_path)
            except errors.FileError:
                self.tgt_lang = update_language_code()
                self.save(file_name, save_path, self.tgt_lang)
        else:
            self.tgt_lang = update_language_code()

    @ staticmethod
    @ file_check
    def load(file_name, path) -> Dict[str, Dict[str, str]]:
        """读取配置文件"""
        c_p = ConfigParser()
        c_p.read(os.path.join(path, file_name), encoding='UTF-8')

        return {i: dict(c_p.items(i)) for i in c_p.sections()}

    @ staticmethod
    def save(file_name, path, data_table: Dict[str, Dict[str, str]]):
        c_p = ConfigParser()
        c_p.read(path, encoding='UTF-8')

        for section in data_table.keys():
            for option in data_table[section].keys():
                try:
                    c_p.set(section, option, data_table[section][option])
                except NoSectionError:
                    c_p.add_section(section)
                    c_p.set(section, option, data_table[section][option])

        path = Path(path)

        if not path.is_dir():
            path.mkdir()

        full_path = os.path.join(path, file_name)
        with open(full_path, 'w', encoding='UTF-8') as file:
            c_p.write(file)

    @ staticmethod
    def template_of_translator(fromlang, tolang, text) -> dict:
        return {
            'url': TRANSLATOR_ENGINE_URL,
            'headers': HEADERS,
            'data': {
                'fromLang': fromlang,
                'to': tolang,
                'text': text,
            }
        }

    @staticmethod
    def template_of_semantic(fromlang, tolang, text):
        return {
            'url': SEMANTIC_URL,
            'headers': HEADERS,
            'data': {
                'from': fromlang,
                'to': tolang,
                'text': text,
            }
        }
