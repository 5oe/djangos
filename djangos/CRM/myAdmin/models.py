from django.db import models


# Create your models here.

class TestAdminInfo(models.Model):
    title = models.CharField(max_length=10, verbose_name='测试标题', default='测试')

    class Meta:
        db_table = 'TestAdminInfo'
        verbose_name_plural = '用于测试admin的表'

    def __str__(self):
        return self.title
