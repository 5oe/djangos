from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UsrInfo)
# admin.site.register(BillInfo)
admin.site.register(BlogInfo)
admin.site.register(Star2Fans)
admin.site.register(KindInfo)
admin.site.register(TagInfo)
# admin.site.register(ArticleInfo)
admin.site.register(Article2Tag)
admin.site.register(EvaluateInfo)


# admin.site.register(CommentInfo)


class TroubleAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/lang/zh_CN.js',
            '/static/js/kindeditor/config.js',
        )


admin.site.register(TroubleInfo, admin_class=TroubleAdmin)


class ArticleAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/lang/zh_CN.js',
            '/static/js/kindeditor/config.js',
        )


admin.site.register(ArticleInfo, admin_class=ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/lang/zh_CN.js',
            '/static/js/kindeditor/config.js',
        )


admin.site.register(CommentInfo, admin_class=CommentAdmin)
