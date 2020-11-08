import unittest
import time
import os

from faker import Faker
import requests

from bing_translation_for_python import core, setting


class Translate(unittest.TestCase):
    def setUp(self):
        self.default_language = 'en'
        self.faker_data = Faker(locale='zh_CN')
        self.tar = core.Translator(self.default_language)

        # texts
        self.text = '你好'
        self.some_text = [self.faker_data.color_name()
                          for i in range(5)]
        self.color_names = [self.faker_data.color_name() for i in range(5)]

    def tearDown(self):
        pass

    def test_translator_with(self):
        tolang = 'zh-Hans'
        with core.Translator(tolang) as translator:
            for text in [self.faker_data.color_name() for i in range(2)]:
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
        t_text = self.tar.translator(
            text='_'.join(self.color_names),
            exclude_s='_'
        )

        self.assertEqual(
            t_text.text(),
            ' '.join(self.color_names),
            '功能：分割参数接受字符功能被破坏'
        )

        # 分割参数接受一个序列
        t_text = self.tar.translator(
            text='><'.join(self.color_names),
            exclude_s=('>', '<')
        )

        self.assertEqual(
            t_text.text(),
            ' '.join(self.color_names),
            '功能：分割参数接受序列功能被破坏'
        )

    def test_translator_return_is_text_obj(self):
        obj = self.tar.translator(self.text)
        self.assertTrue(
            isinstance(obj, core.Text),
            type(obj)
        )

    def test_json(self):
        """测试json方法是否有效"""
        t_text = self.tar.translator(self.text)

        # 实际调用返回对象的 ‘.json’方法
        self.assertTrue(
            isinstance(t_text.json(), list),
            t_text.json()
        )


class Semantic(unittest.TestCase):

    def setUp(self):
        self.tar = core.Translator('en').translator('你好')
        self.semantic = self.tar.semantic()

    def test_text_obj_semantic_return_is_semantic_obj(self):
        """Text对象的semantic方法返回Semantic对象"""
        self.assertTrue(
            isinstance(self.tar, core.Text),
            type(self.tar)
        )
        self.assertTrue(
            isinstance(self.semantic, core.Semantic),
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
            isinstance(i, core.SemanticItem)

    def test_attr(self):
        """Semantici必须包含的属性"""
        semantic = core.Translator('zh-Hans').translator('Hello').semantic()

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


class Core(unittest.TestCase):

    def setUp(self):
        self.test_ini_path = os.path.join(setting.BASE_DIR_OUTSIDE, 'test.ini')
        # 翻译函数请求数据
        self.d_t = {
            "url": ''.join(['https://cn.bing.com/',
                            'ttranslatev3?isVertical=1&',
                            '&IG=ECCC2E222205418FB249C51DB6C943BF&',
                            'IID=translator.5028.1'
                            ]),
            "headers": {
                "user-agent": ' '.join([
                    'Mozilla/5.0',
                    '(Windows NT 10.0; Win64; x64)',
                    'AppleWebKit/537.36',
                    '(KHTML, like Gecko)',
                    'Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66'
                ])
            },
            'data': {
                "fromLang": "auto-detect",
                "to": "zh-Hans",
                "text": None
            }
        }

    def translator(self, text, lang_code):
        """翻译函数接口"""
        self.d_t["data"]["text"] = text
        self.d_t["data"]["to"] = lang_code
        res = requests.post(**self.d_t).json()
        try:
            return res[0]['translations'][0]['text']
        except KeyError as error:
            print(res)
            raise error

    def test_can_save_setting(self):
        path = self.test_ini_path
        try:
            data_table1 = {'test': {'test1': 'test2'}}
            setting.Conf.save_ini(path, data_table1)
            self.assertEqual(data_table1, core.Conf.read_inf('test.ini'))

            data_table2 = {'test3': {'test4': 'test5'}}
            setting.Conf.save_ini(path, data_table2)
            self.assertIn('test3', core.Conf.read_inf(path))
            self.assertIn('test', core.Conf.read_inf(path))

        finally:
            os.system(F'del {path}')

    def test_update_language_code_and_save(self):
        """更新语言 tgt"""
        tgt_lan_of_net_work = core.update_language_code()
        tgt_lag_of_file = core.Conf.read_inf(setting.LANGUAGE_CODE_PATH)

        self.assertEqual(tgt_lag_of_file, tgt_lan_of_net_work)


if __name__ == "__main__":
    unittest.main()
