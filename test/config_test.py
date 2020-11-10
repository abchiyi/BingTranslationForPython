"""配置文件生成测试"""

import unittest
import pathlib
import shutil
import os

from bing_translation_for_python import core, setting

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
test_files_dir = os.path.join(BASE_DIR, 'test_files')


class Config(unittest.TestCase):

    def tearDown(self):
        # 清扫文件
        try:
            shutil.rmtree(test_files_dir)
        except FileNotFoundError:
            pass

    def test_init_config_file(self):
        config = setting.Config(test_files_dir)
        # Translator 接受 config对象作为参数
        core.Translator('en', config=config)

        # 检测文件夹是否被自动创建
        files_dir = pathlib.Path(test_files_dir)
        files = os.listdir(files_dir)
        if not(files_dir.is_dir() and len(files) > 0):
            self.fail("没有找到本地配置文件文件")
