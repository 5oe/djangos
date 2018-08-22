from django.contrib import admin
from .models import *


class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'outline', 'cyc']
    list_filter = ['title', 'price', 'cyc']
    search_fields = ['title', 'price', 'cyc']


# Register your models here.
admin.site.register(UserInfo)
admin.site.register(RoleInfo)
admin.site.register(CustomerInfo)
admin.site.register(CustomerFollowUpInfo)
admin.site.register(ClsInfo)
admin.site.register(MenuInfo)
admin.site.register(SchoolInfo)
# admin.site.register(StudentInfo)
admin.site.register(ScoreInfo)
admin.site.register(QuestionInfo)
admin.site.register(AnswerInfo)
admin.site.register(CourseInfo, CourseInfoAdmin)
admin.site.register(LectureInfo)
