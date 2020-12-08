## 快速开始
从pip工具安装它,在控制台中键入:

    pip install bing-translation-for-python


### 示例
以下是一个简单的展示代码

新建文件`hello.py`,并在其中键入以下代码:
```python
from bing_translation_for_python import Translator

text = Translator('en').translator('你好')

print(text)
```
保存并执行`hello.py`,你能够在控制台中输出了` hello.`<br>

<!-- TODO 未定义的url链接-->
### [*Translation*]()类
想要翻译文本你首先需要实例化一个*Translation*对象,并提供一个必要参数来设定你想要翻译到的语言.<br>例如你想要将一段文本翻译到英语.
```python
Translator(to_lang='en')
```
这个参数仅支持固定的值,支持列表[在这里查看]().<br>
*Translator*还接受一个*Config*对象来定义一些可选设置,[在这里查看]()
