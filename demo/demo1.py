from bing_translation_for_python.core import Translator

# Translator 类默认接受一个语言标签，例如'en'代表英语,'zh-Hans'代表中文简体
# 完成对该对象的初始化之后，可以调用其'translator'方法。任何支持翻译的语言都会被
# 翻译到之前指定的语言
translator = Translator('zh-Hans')

# 该翻译方法最少接受一个'str'参数
text_obj = translator.translator("Hello")
print(text_obj)
