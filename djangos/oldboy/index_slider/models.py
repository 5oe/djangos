from django.db import models


# Create your models here.
class SliderInfo(models.Model):
    img = models.ImageField(upload_to='upload/Slider', verbose_name='图片')
    href = models.CharField(max_length=250, verbose_name='链接')
    title = models.CharField(max_length=20, verbose_name='标题')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    status = models.IntegerField(choices=[(0, '下线'), (1, '上线')], default=1, verbose_name='状态')

    class Meta:
        db_table = 'SliderInfo'
        verbose_name_plural = '首页轮播表'

    def __str__(self):
        return self.title


class NoticeType(models.Model):
    type = models.CharField(max_length=20, verbose_name='公告类型')

    class Meta:
        db_table = 'NoticeType'
        verbose_name_plural = '公告类型表'

    def __str__(self):
        return self.type


class NoticeInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='公告标题')
    content = models.CharField(max_length=1200, verbose_name='公告内容')
    type = models.ForeignKey('NoticeType', on_delete=models.CASCADE, verbose_name='公告类型')
    weight = models.IntegerField(default=0, verbose_name='权重')

    class Meta:
        db_table = 'NoticeInfo'
        verbose_name_plural = '公告表'

    def __str__(self):
        return self.title


class CourseType(models.Model):
    type = models.CharField(max_length=20, verbose_name='课程类型')

    class Meta:
        db_table = 'CourseType'
        verbose_name_plural = '课程类型表'

    def __str__(self):
        return self.type


class CourseInfo(models.Model):
    title = models.CharField(max_length=20, unique=True, verbose_name='课程标题', blank=False)
    img = models.ImageField(upload_to='upload/course', verbose_name='图片')
    content = models.CharField(max_length=1200, verbose_name='课程描述')
    level = models.IntegerField(choices=[(1, '初级'), (2, '中级'), (3, '高级'), (4, '骨灰级')], default=1, verbose_name='课程等级')
    weight = models.IntegerField(default=0, verbose_name='权重')

    class Meta:
        db_table = 'CourseInfo'
        verbose_name_plural = '课程表'

    def __str__(self):
        return self.title


class DirectType(models.Model):
    type = models.CharField(max_length=20, verbose_name='方向')

    class Meta:
        db_table = 'DirectType'
        verbose_name_plural = '方向类型表'

    def __str__(self):
        return self.type


class Course2Direct(models.Model):
    course = models.ForeignKey('CourseInfo', on_delete=models.CASCADE, verbose_name='课程')
    direct = models.ForeignKey('DirectType', on_delete=models.CASCADE, verbose_name='方向')

    class Meta:
        db_table = 'Course2Direct'
        verbose_name_plural = '课程与方向关系表'
        unique_together = ('course', 'direct')

    def __str__(self):
        return self.course.title + '+' + self.direct.type


class Course2Type(models.Model):
    course = models.ForeignKey('CourseInfo', on_delete=models.CASCADE, verbose_name='课程')
    type = models.ForeignKey('CourseType', on_delete=models.CASCADE, verbose_name='课程类型')

    class Meta:
        db_table = 'Course2Type'
        verbose_name_plural = '课程与课程类型关系表'
        unique_together = ('course', 'type')

    def __str__(self):
        return self.course.title + '+' + self.type.type


class StudentInfo(models.Model):
    name = models.CharField(max_length=10, verbose_name='姓名', unique=True, blank=False)
    birthday = models.DateField(verbose_name='生日')
    company = models.CharField(max_length=50, verbose_name='工作所在公司名称')
    salary = models.IntegerField(verbose_name='薪资')
    img = models.ImageField(upload_to='upload/student', verbose_name='图片')

    class Meta:
        db_table = 'StudentInfo'
        verbose_name_plural = '学员表'

    def __str__(self):
        return self.name


class StudentThanksInfo(models.Model):
    student = models.ForeignKey('StudentInfo', on_delete=models.CASCADE, unique=True, verbose_name='学员')
    content = models.CharField(max_length=1200, verbose_name='感谢描述', blank=False)

    class Meta:
        db_table = 'StudentThanksInfo'
        verbose_name_plural = '学员感谢信息表'

    def __str__(self):
        return self.student.name + '的感谢信'


class RecruitInfo(models.Model):
    title = models.CharField(max_length=50, verbose_name='招聘标题', blank=False)
    content = models.CharField(max_length=1200, verbose_name='详细内容')
    salary = models.IntegerField(verbose_name='薪资')
    start_date = models.DateTimeField(verbose_name='发布日期')
    end_date = models.DateTimeField(verbose_name='过期日期', null=True)

    class Meta:
        db_table = 'RecruitInfo'
        verbose_name_plural = '招聘信息发布表'

    def __str__(self):
        return self.title


class LifeInfo(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='标题')
    content = models.CharField(max_length=1200, verbose_name='具体描述')
    img = models.ImageField(upload_to='upload/life', verbose_name='图片')

    class Meta:
        db_table = 'LifeInfo'
        verbose_name_plural = '学员生活表'

    def __str__(self):
        return self.title


class EnterpriseInfo(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='企业名')
    content = models.CharField(max_length=1200, verbose_name='描述内容')
    img = models.ImageField(upload_to='upload/enterprise', verbose_name='图片')
    href = models.CharField(max_length=250, verbose_name='链接')

    class Meta:
        db_table = 'EnterpriseInfo'
        verbose_name_plural = '企业表'

    def __str__(self):
        return self.title
