import os
import sys
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from .Base import Usr
from conf.setting import DB_DIR
from .student import Student
from .cls2Teacher import Cls2Teacher
from .classRecord import ClassRecord
from .score import Score


class Teacher(Usr):
    def __init__(self, uaccount, upwd, owner_school):
        super().__init__(uaccount, upwd)
        self.owner_school = owner_school

    def __str__(self):
        return '(讲师)%s的%s老师' % (self.owner_school, self.uaccount)

    def __get_classes(self):
        c2t_list = []
        c2t_db_path = os.path.join(DB_DIR, 'Stu2Teacher')
        for f_path in os.listdir(c2t_db_path):
            c2t_list.append(Cls2Teacher.load(f_path))

        res = []
        for item in c2t_list:
            if item.owner_teacher == self:
                res.append(item.owner_class)
        return res

    def __get_students(self):
        all_stus = []
        my_classes = self.__get_classes()
        stu_db_path = os.path.join(DB_DIR, 'Student')
        for f_path in os.listdir(stu_db_path):
            all_stus.append(Student.load(f_path))

        my_stus = []
        for stu in all_stus:
            if stu.owner_class in my_classes:
                my_stus.append(stu)
        return my_stus

    def show_classes(self):
        classes = self.__get_classes()
        for i, obj in enumerate(classes):
            print(i + 1, obj)
        return classes

    def show_classes_students(self):
        my_stus = self.__get_students()
        for i, v in enumerate(my_stus):
            print(i + 1, v)
        return my_stus

    def go_to_class(self):
        classes = self.show_classes()
        try:
            ch = input('请输入你要上的课的编号: ')
            next_cls = classes[ch - 1]
            record = ClassRecord(self, next_cls, time.strftime('%Y-%m-%d %X'))
            record.save()
            print('生成上课记录成功，你可以去上课了')
        except Exception as e:
            print('发生错误，错误信息：%s,系统退出' % e)
            return

    def corrent_homework(self):
        stus = self.__get_students()
        try:
            for stu in stus:
                grade = int(input('请输入分数'))
                if grade < 0 or grade > 100:
                    grade = 0
                subject = stu.owner_class.owner_subject
                t = time.strftime("%Y-%m-%d %X")
                score = Score(subject, stu, t, grade)
                score.save()
                print('批改%s同学作业成功' % stu.uname)
        except Exception as e:
            print('发生异常，异常信息：%s，系统退出' % e)
            return
