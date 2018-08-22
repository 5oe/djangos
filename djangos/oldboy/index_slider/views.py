from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import *


# Create your views here.

def index(request):
    # 获得轮播图
    slider_objs = SliderInfo.objects.all().filter(status=1).order_by('-create_date')
    # 获得公告集合
    notice_objs = NoticeInfo.objects.all().order_by('-weight')[:3]
    #  获得课程集合
    course_objs = CourseInfo.objects.all().order_by('-weight')[:6]
    # 获得学员集合
    student_objs = StudentInfo.objects.all().order_by('birthday')
    student_top = student_objs[0]
    student_objs = student_objs[1:5]
    tmp = student_top.studentthanksinfo_set.all()
    star_student_thanks = tmp[0] if tmp else ''

    # 获得招聘信息集合
    recruit_obs = RecruitInfo.objects.all()[:1]

    # 获得学校生活集合
    life_objs = LifeInfo.objects.all()[:4]

    # 获得企业集合
    enterprise_objs = EnterpriseInfo.objects.all()[:4]
    context = {
        'title': '首页',
        'sliders': slider_objs,
        'notices': notice_objs,
        'courses': course_objs,
        'star_student': student_top,
        'star_thanks': star_student_thanks,
        'students': student_objs,
        'recruits': recruit_obs,
        'lifes': life_objs,
        'enterprises': enterprise_objs,
    }
    return render(request, 'index_slider/index.html', context)


def student_job(request):
    return render(request, 'index_slider/stu.html')


def students(request):
    from django.db import connection, transaction
    cursor = connection.cursor()

    # 数据修改操作——提交要求
    cursor.execute('''SELECT
      stu.id,
      stu.name,
      stu.birthday,
      stu.img,
      stu.salary,
      stu.company,
      tk.content
    FROM StudentInfo AS stu LEFT JOIN StudentThanksInfo AS tk ON stu.id = tk.student_id''')
    row = cursor.fetchall()
    print(len(row))
    return JsonResponse(row, safe=False)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CustomPaginator(Paginator):
    def __init__(self, current_page, max_pager_num, *args, **kwargs):
        """
        :param current_page: 当前页
        :param max_pager_num:最多显示的页码个数
        :param args:
        :param kwargs:
        :return:
        """
        self.current_page = int(current_page)
        self.max_pager_num = max_pager_num
        super(CustomPaginator, self).__init__(*args, **kwargs)

    def page_num_range(self):
        # 当前页面
        # self.current_page
        # 总页数
        # self.num_pages
        # 最多显示的页码个数
        # self.max_pager_num
        print(1)
        if self.num_pages < self.max_pager_num:
            return range(1, self.num_pages + 1)
        print(2)
        part = int(self.max_pager_num / 2)
        if self.current_page - part < 1:
            return range(1, self.max_pager_num + 1)
        print(3)
        if self.current_page + part > self.num_pages:
            return range(self.num_pages + 1 - self.max_pager_num, self.num_pages + 1)
        print(4)
        return range(self.current_page - part, self.current_page + part + 1)


def courses(request, direct, type, level):
    # 获得课程类型
    type_objs = CourseType.objects.all()
    # 获得方向
    direct_objs = DirectType.objects.all()
    # 等级
    level_objs = {1: '初级', 2: '中级', 3: '高级', 4: '骨灰级'}

    type = int(type)
    direct = int(direct)
    level = int(level)

    conditions = {}
    if level: conditions['level'] = level
    if direct: conditions['course2direct__direct_id'] = direct
    if type: conditions['course2type__type_id'] = type

    course_objs = CourseInfo.objects.filter(**conditions)

    current_page = request.GET.get('p', 0)
    paginator = CustomPaginator(current_page, 10, course_objs, 1)

    try:
        page = paginator.page(current_page)
        # has_next              是否有下一页
        # next_page_number      下一页页码
        # has_previous          是否有上一页
        # previous_page_number  上一页页码
        # object_list           分页之后的数据列表
        # number                当前页
        # paginator             paginator对象
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'type': int(type),
        'direct': int(direct),
        'level': int(level),
        'types': type_objs,
        'directs': direct_objs,
        'levels': level_objs,
        'courses': course_objs,
        'page': page,
    }
    return render(request, 'index_slider/cls.html', context)
