from django.db import models
from . import *


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
        return '%s 校区' % self.title


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
        return '%s-%s 班' % (self.school.title, self.course.title,)
