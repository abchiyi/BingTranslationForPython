from . import core, setting
from .public import errors


class Translator:
    """必应翻译"""

    def __init__(self, to_lang: str, config: setting.Config = False):

        # 不带参数实例化的Config类,极慢的实例化时间
        if not config:
            config = setting.Config()
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
                   exclude_s: str = None) -> core.Text:
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

        return core.Text(self.to_lang, format_text(exclude_s, text))
