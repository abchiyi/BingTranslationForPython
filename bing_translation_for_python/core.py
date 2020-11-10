import collections
import os

import requests

from .public import errors

from .setting import Config


def file_check(func):
    def run(path, *argv, **kwargs):
        if os.access(path, os.F_OK) and os.access(path, os.R_OK):
            return func(path, *argv, **kwargs)
        raise FileNotFoundError(
            F'没有找到配置文件，或文件不可访问： \n{path}'
        )

    return run


def equal_language_check(func):
    """检查from与to语言代码是否相等"""

    def run(self, from_lang, to_lang, reper_text):
        if from_lang == to_lang:
            raise errors.EqualTextLanguage(F"({from_lang}):{reper_text}")
        return func(self, from_lang, to_lang, reper_text)

    return run


SemanticItem = collections.namedtuple('SemanticItem', ['text', 'semantic'])


class Semantic:

    @equal_language_check
    def __init__(self, from_lang, to_lang, reper_text):
        self.reper_text = reper_text
        self.from_lang = from_lang
        self.to_lang = to_lang

        template = Config.template_of_semantic(
            fromlang=from_lang,
            text=reper_text,
            tolang=to_lang,
        )

        self.__data__ = requests.post(
            **template
        ).json()[0]['translations']

    def __repr__(self):
        return F'"{self.reper_text}"({self.from_lang})-->({self.to_lang})'

    def text(self) -> str:
        data = self.json()['semantic']
        text = '\n'.join([F'{k}:{",".join(v)}' for k, v in data.items()])
        return text

    def json(self) -> dict:
        semantics = {}
        for i in self.__data__:
            temp = []
            for i_i in i['backTranslations']:
                temp.append(i_i['displayText'])
            semantics[i['displayTarget']] = temp
        return {
            'from': self.from_lang,
            'semantic': semantics,
            'to': self.to_lang
        }

    def __getitem__(self, key):
        item = self.__data__[key]
        return SemanticItem(
            item['displayTarget'],
            [i['displayText'] for i in item['backTranslations']]
        )

    def __len__(self):
        return len(self.__data__)


class Text:
    def __init__(self, to_lang, reper_text, fromlang='auto-detect',):
        if reper_text.strip():
            data = requests.post(
                **Config.template_of_translator(
                    fromlang=fromlang,
                    text=reper_text,
                    tolang=to_lang,
                )).json()
        else:
            raise errors.EmptyTextError(F'无效的字符串:"{reper_text}"')

        self.__data__ = data
        self.from_lang = data[0]['detectedLanguage']['language']
        self.reper_text = reper_text
        self.to_lang = to_lang

    def __repr__(self):
        return self.text()

    def json(self) -> dict:
        return self.__data__

    def text(self) -> str:
        texts = []
        for item in self.json():
            for text_item in item['translations']:
                texts.append(text_item['text'])

        return ' '.join(texts)

    def semantic(self) -> Semantic:
        return Semantic(
            self.json()[0]['detectedLanguage']['language'],
            self.to_lang,
            self.reper_text
        )


class Translator:
    """必应翻译"""

    def __init__(self, to_lang: str, config: Config = False):

        # 不带参数实例化的Config类,极慢的实例化时间
        if not config:
            config = Config()
        # 语言标签支持性检查
        if to_lang not in config.tgt_lang:
            raise errors.TargetLanguageNotSupported(F"不支持的语言:{to_lang}")

        self.to_lang = to_lang

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO 也许可以在这里设置打扫运行文件
        pass

    def __repr__(self):
        return str(
            F"<Translator({self.to_lang})>"
        )

    def translator(self,
                   text: str = '',
                   exclude_s: str = None) -> Text:
        """翻译方法"""

        def format_text(strings, texts) -> str:
            """格式化字符串"""

            if isinstance(strings, str):
                strings = [strings.strip()]
            elif isinstance(strings, (list, tuple)):
                strings = [value.strip()
                           for value in strings if isinstance(value, str)]
            else:
                strings = []

            for i in strings:
                texts = ' '.join(texts.replace(i, ' ').split())
            return texts

        return Text(self.to_lang, format_text(exclude_s, text))
