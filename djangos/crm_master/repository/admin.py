from .models import *
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from form.account.user import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'role')}),
        ('Permissions', {'fields': ('is_admin', 'user_permissions', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('role',)


# Now register the new UserAdmin...
admin.site.register(UserInfo, UserAdmin)
admin.site.unregister(Group)

'''
其他表
'''


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
admin.site.register(CustomerDetailInfo)
admin.site.register(ContractTemplateInfo)
admin.site.register(PaymentRecordInfo)
admin.site.register(Group)
admin.site.register(Permission)
