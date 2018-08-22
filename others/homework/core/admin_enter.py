#!/usr/bin/env python
# coding=utf-8
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from lib import bin
from modules.schoool import School
from modules.teacher import Teacher
from modules.subject import Subject
from modules.classes import Class


def admin_view():
    while True:
        print('1.创建学校')
        print('2.创建讲师')
        print('3.创建课程')
        print('4.创建班级')
        print('q.退出')

        ch = input('请输入操作选项： ')
        if ch == 'q':
            return

        elif ch == '1':
            # 创建学校没有任何顾忌
            # schools = bin.get_objs(School)
            name = input('请输入新学校的名字: ')
            # for school in schools:
            #     if school.sname == name:
            #         print('学校名已经存在')
            #         return
            area = input('请输入所在地区: ')
            s = School(name, area)
            s.save()
            print('创建学校成功，新学校为%s' % s)

        elif ch == '2':
            # 创建讲师，若学校集合为空，则不能创建
            schools = bin.get_objs(School)
            if len(schools) < 1:
                print("学校集合为空，请先去创建学校")
                return
            bin.show_enum(schools)
            try:
                ch = int(input('请输入讲师所属学校编号: '))
                school = schools[ch - 1]

            except Exception as e:
                print('学校编号输入错误')
                return

            uname = input('请输入讲师名称： ')
            upwd1 = input('请输入讲师的密码：')
            upwd2 = input('请输入确认密码： ')
            if upwd1 != upwd2:
                print('两次密码不同')
                return
            t = Teacher(uname, upwd1, school)
            t.save()
            print('创建讲师成功')

        elif ch == '3':
            schools = bin.get_objs(School)
            if len(schools) < 1:
                print("学校集合为空，请先去创建学校")
                return
            bin.show_enum(schools)
            try:
                ch = int(input('请输入课程所属学校编号: '))
                school = schools[ch - 1]

            except Exception as e:
                print('学校编号输入错误')
                return

            uname = input('请输入课程名称： ')
            cyc_days = input('请输入课程周期： ')
            sprice = input('请输入价格： ')
            s = Subject(uname, cyc_days, sprice, school)
            s.save()
            print('创建课程成功')

        elif ch == '4':
            schools = bin.get_objs(School)
            subjects = bin.get_objs(Subject)
            if len(schools) < 1:
                print("学校集合为空，请先去创建学校")
                return

            if len(subjects) < 1:
                print('课程集合为空，请先去创建课程')
                return
            bin.show_enum(schools)
            try:
                ch = int(input('请输入班级所属学校编号: '))
                school = schools[ch - 1]

            except Exception as e:
                print('学校编号输入错误')
                return
            filter_subjects = []
            for s in subjects:
                if str(s.owner_school) == str(school):
                    filter_subjects.append(s)

            if len(filter_subjects) < 1:
                print('抱歉，该学校还没有设立课程')
                return

            bin.show_enum(filter_subjects)
            try:
                ch = int(input('请输入班级所属课程编号: '))
                subject = subjects[ch - 1]
            except Exception as e:
                print('课程编号输入错误')
                return

            cname = input('请输入班级名称： ')
            c = Class(cname, subject, school)
            c.save()
            print('课程班级成功')
        else:
            print('选项输入错误')
