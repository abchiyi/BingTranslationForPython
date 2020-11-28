import unittest
import time

from faker import Faker

from bing_translation_for_python import Translator
from bing_translation_for_python.core import Text, Semantic, SemanticItem


class TranslateTest(unittest.TestCase):
    def setUp(self):
        self.default_language = 'en'
        self.faker = Faker(locale='zh_CN')
        self.tra = Translator(self.default_language)

        # texts
        self.text = '你好'
        self.some_text = [self.faker.color_name() for i in range(5)]

    def tearDown(self):
        pass

    def test_translator_with(self):
        tolang = 'zh-Hans'
        with Translator(tolang) as translator:
            for text in [self.faker.color_name() for i in range(2)]:
                self.assertTrue(
                    isinstance(translator.translator(text).text(), str)
                )
                time.sleep(0.5)

    def test_split_string(self):
        """
        字符串包含翻译引擎无法识别的字符时,指定分割符,
        以及确保对象方法的参数有效
        """

        # 分割参数接受字符串
        t_text = self.tra.translator(
            text='_'.join(self.some_text),
            exclude_s='_'
        )

        self.assertEqual(
            t_text.text(),
            ' '.join(self.some_text),
            '功能：分割参数接受字符功能被破坏'
        )

        # 分割参数接受一个序列
        t_text = self.tra.translator(
            text='><'.join(self.some_text),
            exclude_s=('>', '<')
        )

        self.assertEqual(
            t_text.text(),
            ' '.join(self.some_text),
            '功能：分割参数接受序列功能被破坏'
        )

    def test_translator_return_is_text_obj(self):
        obj = self.tra.translator(self.text)
        self.assertTrue(
            isinstance(obj, Text),
            type(obj)
        )

    def test_json(self):
        """测试json方法是否有效"""
        t_text = self.tra.translator(self.text)

        # 实际调用返回对象的 ‘.json’方法
        self.assertTrue(
            isinstance(t_text.json(), list),
            t_text.json()
        )


class SemanticTest(unittest.TestCase):

    def setUp(self):
        self.tar = Translator('en').translator('你好')
        self.semantic = self.tar.semantic()

    def test_text_obj_semantic_return_is_semantic_obj(self):
        """Text对象的semantic方法返回Semantic对象"""
        self.assertTrue(
            isinstance(self.tar, Text),
            type(self.tar)
        )
        self.assertTrue(
            isinstance(self.semantic, Semantic),
            type(self.semantic)
        )

    def test_json_method(self):
        """Semantic对象包含json方法"""
        data = self.semantic.json()

        self.assertTrue(isinstance(data, dict), type(data))

        if ('to' not in data) and ('from' not in data):
            self.fail('json方法返回字典必要的条目')

        self.assertEqual(type(data['semantic']), dict, data)

    def test_text_method(self):
        """Semantic对象包含text方法"""
        data = self.semantic.json()['semantic']
        text = self.semantic.text()

        for key in data:
            if key not in text:
                self.fail(F'{key}未包含')

        self.assertTrue(isinstance(text, str), type(text))

    def test_is_iterative(self):
        """Semantic对象是可迭代的"""
        for i in self.semantic:
            isinstance(i, SemanticItem)

    def test_attr(self):
        """Semantici必须包含的属性"""
        semantic = Translator('zh-Hans').translator('Hello').semantic()

        try:
            print(semantic.from_lang)
            print(semantic.to_lang)
        except AttributeError as error:
            self.fail(F'{error}需要包含的属性')

    def test_smeantic_have_len(self):
        try:
            len(self.semantic)
        except TypeError:
            self.fail('semantic 没有__len__方法')
