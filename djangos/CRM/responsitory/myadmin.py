import myAdmin as admin
from myAdmin.acquirer.modelAdmin import ModelAdmin
from .models import *


class CourseInfoAdmin(ModelAdmin):
    list_display = ['title', 'price', 'outline', 'cyc']
    list_filter = ['title', 'price', 'cyc']
    search_fields = ['title', 'price', 'cyc']
    readonly_fields = ['title']


class ScoreInfoAdmin(ModelAdmin):
    list_display = ['student', 'lecture', 'grade', 'student_status', 'note', 'date']
    list_filter = ['student', 'lecture', 'grade', 'student_status', 'note', 'date']
    search_fields = ['grade', 'student_status', 'note', 'date']
    readonly_fields = ['student', 'lecture', 'grade']


class CustomerInfoAdmin(ModelAdmin):
    list_filter = ['time', 'source', 'contact', 'consultant', 'status', 'consult_content',
                   'introduce_customer']
    list_display = ['time', 'source', 'contact', 'consultant', 'status', 'consult_content',
                    'introduce_customer']
    search_fields = ['time', 'source', 'contact', 'consultant', 'status', 'consult_content',
                     'introduce_customer']

    readonly_fields = ['time', 'contact', 'consultant', 'status']


# Register your models here.
admin.site.register(UserInfo)
admin.site.register(RoleInfo)
admin.site.register(CustomerInfo, CustomerInfoAdmin)
admin.site.register(MenuInfo)
admin.site.register(SchoolInfo)
admin.site.register(ScoreInfo, ScoreInfoAdmin)
admin.site.register(QuestionInfo)
admin.site.register(CourseInfo, CourseInfoAdmin)
admin.site.register(LectureInfo)
