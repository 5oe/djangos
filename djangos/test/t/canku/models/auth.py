from django.db import models
from . import *

# Create your models here.

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
        return '%s 回答 %s' % (self.handler.username, self.question.title)


class ScoreInfo(models.Model):
    grade_choices = [(100, 'A+'), (95, 'A'), (90, 'A-'),
                     (85, 'B+'), (80, 'B'), (75, 'B-'),
                     (70, 'C+'), (65, 'C'), (60, 'C-'),
                     (0, '不及格')]

    student_status_choices = [(0, '缺勤'), (1, '迟到'), (2, '早退'), (3, '出勤')]

    student = models.ForeignKey('StudentInfo', verbose_name='学员')
    lecture = models.ForeignKey('LectureInfo', verbose_name='所属课堂')
    grade = models.PositiveIntegerField(choices=grade_choices, verbose_name='成绩', default=0)
    student_status = models.SmallIntegerField(choices=student_status_choices, verbose_name='出勤状态')
    note = models.TextField(verbose_name='成绩备注', blank=True, null=True)
    date = models.DateField(auto_now_add=True, verbose_name='提交日期')

    class Meta:
        db_table = 'ScoreInfo'
        verbose_name_plural = '成绩表'

    def __str__(self):
        return '%s - %s ' % (self.student.name, self.get_grade_display())


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
