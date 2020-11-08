import argparse
import pathlib
import shutil
import os

FILE_PATH = ['./bing_translation_for_python.egg-info/',
             './build/',
             './dist/'
             ]


def package() -> bool:
    # 获取os执行结果，返回bool类型
    if os.system("python ./setup.py bdist_wheel"):
        return False
    return True


def upload() -> bool:
    # 获取os执行结果，返回bool类型
    if os.system("twine upload ./dist/*"):
        return False
    return True


def clean():
    # 删除打包文件
    for path in FILE_PATH:
        if pathlib.Path(path).is_dir():
            print(F"removing {path}")
            shutil.rmtree(path)


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--package', action='store_true')
parser.add_argument('-u', '--upload', action='store_true')
parser.add_argument('-c', '--clean', action='store_true')


if __name__ == "__main__":
    # 在不提供输入选项时显示帮助选项
    args = os.sys.argv
    if len(args) < 2:
        args = ['-h']
    # 解析选项
    name_space = parser.parse_args(args[1:])
    # 该参数决定'uplaod'和'clean'选项是否执行
    PACKAGE_VALUE = False
    if name_space.package:
        PACKAGE_VALUE = package()
    if name_space.upload and PACKAGE_VALUE:
        upload()
    if name_space.clean:
        clean()
