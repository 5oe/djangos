from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserInfo(models.Model):
    user = models.ForeignKey(User, verbose_name='用户名')
    role = models.ManyToManyField('RoleInfo', verbose_name='角色')
    img = models.ImageField(upload_to='head', verbose_name='头像', blank=True, null=True)
    identity_id = models.CharField(max_length=18, verbose_name='身份证号码', unique=True)

    class Meta:
        db_table = 'UserInfo'
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.user.username


class RoleInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='角色名', unique=True)
    menu = models.ManyToManyField('MenuInfo', verbose_name='菜单', blank=True, null=True)

    class Meta:
        db_table = 'RoleInfo'
        # verbose_name_plural = '角色表'

    def __str__(self):
        return self.title


class CourseInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='课程名')
    price = models.PositiveIntegerField(verbose_name='价格')
    outline = models.TextField(verbose_name='课程大纲')
    cyc = models.PositiveIntegerField(verbose_name='课程周期(月)')

    class Meta:
        db_table = 'CourseInfo'
        verbose_name_plural = '课程表'

    def __str__(self):
        return self.title


class CustomerInfo(models.Model):
    contact_choices = [(0, 'qq'), (1, '微信'), (2, '电话联系')]
    source_choices = [(0, 'qq群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其他论坛')]
    status_choices = [(0, '未报名'), (1, '已报名'), (2, '已退学')]

    name = models.CharField(max_length=20, default='匿名用户')
    time = models.DateTimeField(auto_now_add=True, verbose_name='发掘时间')
    source = models.PositiveIntegerField(choices=source_choices, verbose_name='来源')
    contact = models.PositiveIntegerField(choices=contact_choices, verbose_name='联系方式')
    consultant = models.ForeignKey('UserInfo', verbose_name='课程顾问')
    status = models.PositiveIntegerField(choices=status_choices, verbose_name='状态')
    consult_courses = models.ManyToManyField('CourseInfo', verbose_name='咨询课程')
    consult_content = models.TextField(verbose_name='咨询内容')
    introduce_customer = models.ForeignKey('self', blank=True, null=True, verbose_name='转介绍学员')

    class Meta:
        db_table = 'CustomerInfo'
        verbose_name_plural = '客户表'

    def __str__(self):
        return self.name


class CustomerFollowUpInfo(models.Model):
    status_choices = [
        (0, '近期无报名计划'),
        (1, '一个月内报名'),
        (2, '2周内要报名'),
        (3, '已报名')
    ]
    customer = models.ForeignKey('CustomerInfo', verbose_name='客户')
    content = models.TextField(verbose_name='跟踪内容')
    handler = models.ForeignKey('UserInfo', verbose_name='跟进入')
    status = models.SmallIntegerField(choices=status_choices, verbose_name='状态')
    date = models.DateField(auto_now_add=True, verbose_name='日期')

    class Meta:
        db_table = 'CustomerFollowUpInfo'
        verbose_name_plural = '客户跟踪表'

    def __str__(self):
        return '%s 跟踪 %s' % (self.handler, self.customer.name)


class QuestionInfo(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    detail = models.TextField(verbose_name='问题详述')
    student = models.ForeignKey('UserInfo', verbose_name='提问学生')

    class Meta:
        db_table = 'QuestionInfo'
        verbose_name_plural = '提交问题表'

    def __str__(self):
        return self.title


class AnswerInfo(models.Model):
    question = models.ForeignKey('QuestionInfo', verbose_name='问题')
    handler = models.ForeignKey('UserInfo', verbose_name='回答者')
    time = models.DateTimeField(verbose_name='回答时间')
    up_count = models.PositiveIntegerField(verbose_name='点赞数', default=0)
    down_count = models.PositiveIntegerField(verbose_name='踩数', default=0)

    class Meta:
        db_table = 'AnswerInfo'
        verbose_name_plural = '回答表'

    def __str__(self):
        return '%s 回答 %s' % (self.handler.user.username, self.question.title)


class ScoreInfo(models.Model):
    grade_choices = [(100, 'A+'), (95, 'A'), (90, 'A-'),
                     (85, 'B+'), (80, 'B'), (75, 'B-'),
                     (70, 'C+'), (65, 'C'), (60, 'C-'),
                     (0, '不及格')]

    student_status_choices = [(0, '缺勤'), (1, '迟到'), (2, '早退'), (3, '出勤')]

    student = models.ForeignKey('UserInfo', verbose_name='学员')
    lecture = models.ForeignKey('LectureInfo', verbose_name='所属课堂')
    grade = models.PositiveIntegerField(choices=grade_choices, verbose_name='成绩', default=0)
    student_status = models.SmallIntegerField(choices=student_status_choices, verbose_name='出勤状态')
    note = models.TextField(verbose_name='成绩备注', blank=True, null=True)
    date = models.DateField(auto_now_add=True, verbose_name='提交日期')

    class Meta:
        db_table = 'ScoreInfo'
        verbose_name_plural = '成绩表'

    def __str__(self):
        return '%s - %s ' % (self.student, self.get_grade_display())


class ClsInfo(models.Model):
    cls_type_choices = [(0, '脱产'), (1, '周末'), (2, '网络班')]

    title = models.CharField(max_length=40, verbose_name='班级名', null=True, blank=True)
    course = models.ForeignKey('CourseInfo', verbose_name='所学课程')
    school = models.ForeignKey('SchoolInfo', verbose_name='所属校区')
    semester = models.SmallIntegerField(verbose_name='学期')
    teachers = models.ManyToManyField('UserInfo', verbose_name='教师')
    start_date = models.DateField(verbose_name='开班日期')
    graduate_date = models.DateField(verbose_name='毕业日期')
    type = models.SmallIntegerField(choices=cls_type_choices, verbose_name='班级类型')

    class Meta:
        db_table = 'ClsInfo'
        verbose_name_plural = '班级表'
        unique_together = ['school', 'type', 'course', 'semester']

    def __str__(self):
        return '%s-%s-%s' % (self.school.title, self.course.title, self.title)


class LectureInfo(models.Model):
    cls = models.ForeignKey('ClsInfo', verbose_name='所属课堂')
    teacher = models.ForeignKey('UserInfo', verbose_name='上课老师')
    title = models.CharField(max_length=32, verbose_name='本节主题')
    content = models.TextField(verbose_name='本节主要内容')
    time = models.DateTimeField(auto_now_add=True, verbose_name='上课时间')
    homework = models.TextField(verbose_name='作业需求', blank=True, null=True)

    class Meta:
        db_table = 'LectureInfo'
        verbose_name_plural = '课堂记录表'

    def __str__(self):
        return self.title


class SchoolInfo(models.Model):
    title = models.CharField(max_length=64, verbose_name='学校名')
    address = models.CharField(max_length=128, verbose_name='学校地址')

    class Meta:
        db_table = 'SchoolInfo'
        verbose_name_plural = '校区表'

    def __str__(self):
        return self.title


class MenuInfo(models.Model):
    url_type_choices = [(0, '固定url'), (1, '动态url')]

    title = models.CharField(max_length=64, verbose_name='菜单名')
    url_type = models.SmallIntegerField(choices=url_type_choices, verbose_name='URL类型')
    url_name = models.CharField(max_length=128, verbose_name='URL后缀')

    class Meta:
        db_table = 'MenuInfo'
        verbose_name_plural = '菜单表'

    def __str__(self):
        return self.title
