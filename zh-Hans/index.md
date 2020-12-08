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
* to_lang
    * 这是一个**str**参数,且只接受特定的值,支持列表[在这里查看][1]
* config
    * 这个参数接受[*Config*](api/config)对象,用来定义一些可选设置.

```python
from bing_translation_for_python import Translator

tr = Translator(to_lang='en')
```

#### 翻译文本
现在你已经初始化了一个[*Translator*][2]对象,并将目标语言设定为了英语('en')现在来调用该对象的翻译方法.它将会把任何支持的语言翻译到英语('en').在这里还是使用中文-简体('zh-Hans')来演示
```python
text = tr.translator('你好')
```
**.translator**会返回一个[*Text*][3]对象.它含有两个常用方法来获取数据
* **.text**
    * 这个方法返回排版后的字符串
* **.json**
    * 这个方法返回**json**数据

#### 获取单词的详细释义
你可以对[*Text*][3]对象调用它的 **.semantic**方法,这个方法不需要任何参数.该方法返回一个[*Semantic*][4]对象.
```python
semantics = text.semantic()
```
* [*Semantic*][4]对象支持类似序列的方式来处理它
```python
sem = semantics[1]

for sem in semantics:
    sem.text
    sem.semantic
```

或者你可以通过调用[*Semantic*][4]对象的方法来获取数据
* **.text**
    * 该方法返回排版后的字符串
* **.json**
    * 这个方法返回**json**数据

>其中**Semantic**对象中包含的条目为[*SemanticItem*][4]对象,它实质上是一个*namedtuple*.


## 更多
* 更多详细文档点击[这里](api/)
* 支持语言列表点击[这里][1]

<!-- TODO 终端工具的文档链接和项目地址 -->
## 一个小工具
这是一个终端中的翻译工具,使用pip来安装它.[文档]()&[项目地址]()

    pip install bing-terminal-translator

<!-- 语言支持 -->
[1]:supportedlanguages
<!-- Translator -->
[2]:api/translator
<!-- Text -->
[3]:api/text
<!-- Semantic -->
[4]:api/semantic
