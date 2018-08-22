import myAdmin as admin
from myAdmin.acquirer.modelAdmin import ModelAdmin
from .models import *


class CourseInfoAdmin(ModelAdmin):
    list_display = ['title', 'price', 'outline', 'cyc']
    list_filter = ['title', 'price', 'cyc']
    search_fields = ['title', 'price', 'cyc']


# Register your models here.
admin.site.register(UserInfo)
admin.site.register(RoleInfo)
admin.site.register(CustomerInfo)
admin.site.register(MenuInfo)
admin.site.register(SchoolInfo)
admin.site.register(ScoreInfo)
admin.site.register(QuestionInfo)
admin.site.register(CourseInfo, CourseInfoAdmin)
admin.site.register(LectureInfo)
