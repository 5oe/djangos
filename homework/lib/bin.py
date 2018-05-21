import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf.setting import DB_DIR


def get_objs(cls):
    cls_db_path = os.path.join(DB_DIR, cls.__name__)
    objs = []
    for f_name in os.listdir(cls_db_path):
        f_path = os.path.join(cls_db_path,f_name)
        objs.append(cls.load(f_path))
    return objs


def show_enum(seq):
    for i, k in enumerate(seq):
        print(i + 1, k)
