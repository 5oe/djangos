import os
import sys
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from .Base import Usr
from lib import bin
from modules.schoool import School
from modules.classes import Class
from modules.subject import Subject
from modules.score import Score


class Student(Usr):
    def __init__(self, uaccount, upwd, owner_class=None):
        super().__init__(uaccount, upwd)
        self.owner_class = owner_class

    def __str__(self):
        return '（学员）%s同学' % self.uaccount

    def enroll_to_class(self):
        if self.owner_class is None:
            schools = bin.get_objs(School)
            for i, v in enumerate(schools):
                print(i + 1, v)
            try:
                ch = int(input('请输入你要报名的学校编号： '))
                school = schools[ch - 1]

            except Exception as e:
                print('发生异常，异常信息：%s，系统退出' % e)
                return False

            subs = bin.get_objs(Subject)
            filter_subjects = []
            for sub in subs:
                if str(sub.owner_school) == str(school):
                    filter_subjects.append(sub)
            if len(filter_subjects) < 1:
                print('该学校还没有课程')
                return
            for i, v in enumerate(filter_subjects):
                print(i + 1, v)
            try:
                ch = int(input('请输入你要报名的课程编号： '))
                mysubject = filter_subjects[ch - 1]
                print('正在报名，转到付费中心'.center(50, '*'))
                if self.pay_subject(mysubject):
                    mycls = self.choiced_class(mysubject)
                    if not mycls:
                        return
                    self.owner_class = mycls
                    self.save()
                    print('报名成功了')
                    return True
                else:
                    print('报名失败了')
            except Exception as e:
                print('发生异常，异常信息：%s，系统退出' % e)
                return False
        else:
            print('你已经报名了，被分配的班级家为%s' % self.owner_class)

    def pay_subject(self, subject):
        print('这个课程价格为%s' % subject.sprice)
        print('调用支付接口...')
        print('支付手续中')
        print('支付成功')
        return True

    def choiced_class(self, subject):
        classes = bin.get_objs(Class)
        filter_classes = []
        for cls in classes:
            if str(cls.owner_subject) == str(subject):
                filter_classes.append(cls)

        if len(filter_classes) == 0:
            print('班级为空')
            return False
        return random.choice(filter_classes)

    def __get_scores(self):
        scores = bin.get_objs(Score)
        myscores = []
        for score in scores:
            if score.owner_student == self:
                myscores.append(score)
        return myscores

    def show_scores(self):
        scores = self.__get_scores()
        if len(scores) == 0:
            print('成绩列表为空')
        for i, v in enumerate(scores):
            print(i + 1, v)

    @classmethod
    def register(cls):
        uname = input('请输入你的名称： ')
        stus = bin.get_objs(Student)
        for stu in stus:
            if stu.uaccount == uname:
                print('用户名已存在')
                return
        upwd1 = input('请输入你的密码：')
        upwd2 = input('请再次输入确认密码： ')
        if upwd1 != upwd2:
            print('两次密码不同')
            return
        s = Student(uname, upwd1)
        s.save()
        print('注册学员成功')
        return s
