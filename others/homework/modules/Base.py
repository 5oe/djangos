import os
import sys
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf.setting import DB_DIR


class Base(object):
    def save(self):
        cls_db_path = os.path.join(DB_DIR, self.__class__.__name__)
        if not os.path.exists(cls_db_path):
            os.mkdir(cls_db_path)
        db_path = os.path.join(cls_db_path, str(self))
        with open(db_path, 'wb+')as f:
            f.write(pickle.dumps(self))

    @classmethod
    def load(cls, db_path):
        cls_db_path = os.path.join(DB_DIR, cls.__name__)
        if not os.path.exists(cls_db_path):
            os.mkdir(cls_db_path)
            raise Exception('没有存储的对象，请先存储')
        with open(db_path, 'rb')as f:
            res = pickle.loads(f.read())
        return res


class Usr(Base):
    def __init__(self, uaccount, upwd):
        self.uaccount = uaccount
        self.upwd = upwd
