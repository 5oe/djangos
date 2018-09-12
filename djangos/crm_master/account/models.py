from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

class ArticleManager(models.Manager):
    def distinct_date(self, **kwargs):
        l = self.filter(**kwargs).values('time')
        res = set()
        for obj in l:
            # obj['time']是datetime.datetime对象
            t = obj['time'].strftime('%Y-%m')
            res.add(t)
        return res


class ArticleInfo(models.Model):
    blog = models.ForeignKey('BlogInfo', on_delete=models.CASCADE, verbose_name='所属博客')
    title = models.CharField(max_length=50, verbose_name='文章标题')
    summary = models.TextField(verbose_name='简介', null=True)
    time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    detail = models.TextField(verbose_name='文章内容')
    index_kind = models.IntegerField(choices=[(1, '技术'), (2, '新闻'), (3, '其他')], verbose_name='总分类', default=2)
    read = models.IntegerField(default=0, verbose_name='阅读量')

    objects = ArticleManager()  # 自定义管理器

    class Meta:
        db_table = 'ArticleInfo'
        verbose_name_plural = '文章表'

    def __str__(self):
        return self.title


class BlogInfo(models.Model):
    signature = models.CharField(max_length=30, verbose_name='个性签名')
    title = models.CharField(max_length=10, verbose_name='博客标题')

    class Meta:
        db_table = 'BlogInfo'
        verbose_name_plural = '个人博客表'

    def __str__(self):
        return self.title
