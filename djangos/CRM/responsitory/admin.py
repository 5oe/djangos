from django.contrib import admin
from .models import *


class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'outline', 'cyc']
    list_filter = ['title', 'price', 'cyc', 'outline']
    search_fields = ['title', 'price', 'cyc']


class ScoreInfoAdmin(admin.ModelAdmin):
    list_display = ['student', 'lecture', 'grade', 'student_status', 'note', 'date']
    list_filter = ['student', 'lecture', 'grade', 'student_status', 'note', 'date']
    search_fields = ['grade', 'student_status', 'note', 'date']
    # filter_horizontal = ['student', 'lecture']  # manytomany


class CustomerInfoAdmin(admin.ModelAdmin):
    list_filter = ['time', 'source', 'contact', 'consultant', 'status', 'consult_content',
                   'introduce_customer']
    list_display = ['time', 'source', 'contact', 'consultant', 'status', 'consult_content',
                    'introduce_customer']
    search_fields = ['time', 'source', 'contact', 'consultant', 'status', 'consult_content',
                     'introduce_customer']


    # 定制Action行为具体方法
    def func(self, request, queryset):
        print(self, request, queryset)
        print(request.POST.getlist('_selected_action'))

    func.short_description = "中文显示自定义Actions"
    actions = [func, ]


class ClsInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'school', 'semester', 'start_date', 'graduate_date', 'type']
    search_fields = ['title', 'course', 'school', 'semester', 'start_date', 'graduate_date', 'type']
    list_filter = ['title', 'course', 'school']
    filter_horizontal = ['teachers']


# Register your models here.
admin.site.register(UserInfo)
admin.site.register(RoleInfo)
admin.site.register(CustomerInfo, CustomerInfoAdmin)
admin.site.register(CustomerFollowUpInfo)
admin.site.register(ClsInfo, ClsInfoAdmin)
admin.site.register(MenuInfo)
admin.site.register(SchoolInfo)
# admin.site.register(StudentInfo)
admin.site.register(ScoreInfo, ScoreInfoAdmin)
admin.site.register(QuestionInfo)
admin.site.register(AnswerInfo)
admin.site.register(CourseInfo, CourseInfoAdmin)
admin.site.register(LectureInfo)
