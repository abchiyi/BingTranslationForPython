from setuptools import setup
from os import popen
setup(
    # 从标准输出获取版本号
    version=popen('git tag').read().split()[-1]
)
