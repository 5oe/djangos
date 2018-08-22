#!/usr/bin/env python
# coding=utf-8
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from lib import bin
from modules.student import Student
from conf.setting import login_info


def login(func):
    def wrapper(*args, **kwargs):
        if not login_info['isLogin']:
            print('你还没有登录')
            print('你现在只有两条路，登录1和注册2')
            ch = input('请输入你的选择： ')
            if ch == '1':
                stus = bin.get_objs(Student)
                name = input('请输入你的学员名称')
                flag = False
                for stu in stus:
                    if stu.uaccount == name:
                        pwd = input('请输入你的密码')
                        if stu.upwd == pwd:
                            flag = True
                            print('登录成功')
                            login_info['uaccount'] = stu
                            login_info['isLogin'] = True
                            login_info['type'] = 'Student'
                            return func(*args, **kwargs)
                        else:
                            print('密码错误')
                            return
                if not flag:
                    print('不存在的用户名')
                    return
            elif ch == '2':
                s = Student.register()
                if s is None:
                    return
                login_info['uaccount'] = s
                login_info['isLogin'] = True
                login_info['type'] = 'Student'
                return func(*args, **kwargs)

    return wrapper


@login
def student_view():
    s = login_info['uaccount']
    while True:
        print('学生操作选项'.center(50, '*'))
        print('1.报名课程')
        print('2.查看成绩')
        print('q.退出')
        ch = input('请输入要操作的选项： ')
        if ch == 'q':
            break
        if ch == '1':
            s.enroll_to_class()
        elif ch == '2':
            s.show_scores()
        else:
            print('选项输入错误')

if __name__=='__main__':
    student_view()
