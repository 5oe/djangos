from django.db import models
from . import *


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
        return '%s 回答 %s' % (self.handler.username, self.question.title)


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
