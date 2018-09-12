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

    # 定制Action行为具体方法
    def change_status(self, request, queryset):
        print('全部改为报名')
        row = queryset.update(status=1)
        print('改报名成功情况', row)

    change_status.short_description = "全部改为报名"
    actions = [change_status, ]


class ClsInfoAdmin(ModelAdmin):
    list_display = ['title', 'course', 'school', 'semester', 'start_date', 'graduate_date', 'type']
    search_fields = ['title', 'course', 'school', 'semester', 'start_date', 'graduate_date', 'type']
    list_filter = ['title', 'course', 'school']
    readonly_fields = ['title', 'course', 'school']
    filter_horizontal = ['teachers']


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
admin.site.register(ClsInfo, ClsInfoAdmin)
admin.site.register(CustomerFollowUpInfo)
