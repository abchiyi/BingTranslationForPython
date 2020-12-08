from bing_translation_for_python import Translator

tr = Translator('en')

text = tr.translator('你好')
print(text)
sem = text.semantic()
print(sem)
for i in sem:
    print(i)
