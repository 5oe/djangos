class BlogInfo(models.Model):
    user = models.ForeignKey('UsrInfo', on_delete=models.CASCADE, verbose_name='所属用户')
    surfix = models.CharField(max_length=10, verbose_name='后缀', unique=True)
    signature = models.CharField(max_length=30, verbose_name='个性签名')
    title = models.CharField(max_length=10, verbose_name='博客标题')

    class Meta:
        db_table = 'BlogInfo'
        verbose_name_plural = '个人博客表'

    def __str__(self):
        return self.user.username + '的博客'
