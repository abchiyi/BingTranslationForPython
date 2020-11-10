import unittest
from bing_translation_for_python import core, public


class ErrorsTest(unittest.TestCase):

    def test_file_notfound(self):
        """配置文件读函数在找不到文件时抛出错误"""
        try:
            core.Config.load('sr.ini', './')
        except FileNotFoundError:
            pass
        else:
            self.fail('Not captured:FileNotFoundError')

    def test_not_support_error(self):
        """在给出不受支持的目标语言代码时抛出错误"""
        try:
            core.Translator('abc')
        except public.errors.TargetLanguageNotSupported:
            pass
        else:
            self.fail(
                'Not captured:TargetLanguageNotSupported with "Translator" obj'
            )

    def test_empty_text_error(self):
        """在没有给出文本时的错误"""
        try:
            # 确保字符串仅包含空格时也作为空处理
            core.Translator('en').translator('  ')
        except public.errors.EmptyTextError:
            pass
        else:
            self.fail('Not captured:EmptyTextError')

    def test_language_code_equa_to_the_text_language(self):
        """文本语言与给出的语言码相等时抛出错误"""
        try:
            core.Text('en', 'hello').semantic()
        except public.errors.EqualTextLanguage:
            pass
        else:
            self.fail('Not captured:EqualTextLanguage')
