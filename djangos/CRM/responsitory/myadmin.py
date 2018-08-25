import myAdmin as admin
from myAdmin.acquirer.modelAdmin import ModelAdmin
from .models import *


class CourseInfoAdmin(ModelAdmin):
    list_display = ['title', 'price', 'outline', 'cyc']
    list_filter = ['title', 'price', 'cyc']
    search_fields = ['title', 'price', 'cyc']


class ScoreInfoAdmin(ModelAdmin):
    list_display = ['student', 'lecture', 'grade', 'student_status', 'note', 'date']
    list_filter = ['student', 'lecture', 'grade', 'student_status', 'note', 'date']
    search_fields = ['grade', 'student_status', 'note', 'date']


# Register your models here.
admin.site.register(UserInfo)
admin.site.register(RoleInfo)
admin.site.register(CustomerInfo)
admin.site.register(MenuInfo)
admin.site.register(SchoolInfo)
admin.site.register(ScoreInfo, ScoreInfoAdmin)
admin.site.register(QuestionInfo)
admin.site.register(CourseInfo, CourseInfoAdmin)
admin.site.register(LectureInfo)
