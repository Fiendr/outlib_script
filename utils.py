import os
import sys


def get_exe_dir():
    if getattr(sys, "frozen", False):   # 如果已被打包
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
