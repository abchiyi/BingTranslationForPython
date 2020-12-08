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
保存并执行`hello.py`,你能够看见在控制台中输出了` hello.` .在`hello.py`中将简体中文的文本翻译成为了英语.

<!-- TODO 未定义的url链接-->
#### 初始化*Translation*类
想要翻译文本你首先需要实例化一个*Translation*对象,并提供一个必要参数来设定你想要翻译到的语言.<br>例如你想要将一段文本翻译到英语.
```python
from bing_translation_for_python import Translator

tr = Translator(to_lang='en')
```
这个参数仅支持固定的值,支持列表[在这里查看]().<br>
*Translator*还接受一个*Config*对象来定义一些可选设置,[在这里查看]()

#### 翻译文本
现在你已经初始化了一个*Translator*对象,并将目标语言设定为了英语('en')现在来调用该对象的翻译方法.它将会把任何支持的语言翻译到英语('en').在这里还是使用中文-简体('zh-Hans')来演示
```python
text = tr.translator('你好')
```
*.translator*会返回一个[*Text*]()对象,可以通过它的 **.json**方法获取来自服务器的json数据,亦或者通过 **.text**方法获取格式化后的文本,或是使用**print**函数直接将它打印到控制台

#### 获取单词的详细释义
你可以对*Text*对象调用它的 **.semantic**方法,这个方法不需要任何参数.该方法返回一个[*Semantic*]()对象,它的内部包含了目标语言中对于的解释意思和同义词和近义词等等信息.可以通过类似操作序列的方式获取数据.
```python
semantics = text.semantic()

for sem in semantics:
    print(sem)
```
