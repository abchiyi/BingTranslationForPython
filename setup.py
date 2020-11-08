from setuptools import setup, find_packages
from os import path, popen


with open(path.join('./README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='bing_translation_for_python',
    python_requires='>=3.6',
    # 从标准输出获取版本号
    version=popen('git tag').read().split()[-1],
    author='87Keys',
    author_email='meme_me2019@outlook.com',
    long_description_content_type='text/markdown',
    long_description=open('./README.md', encoding='UTF-8').read(),
    packages=find_packages(),
    classifiers=[
        # "Programming Language:: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        i.strip()
        for i in open('./install_requires').readlines()][:-1]
)
