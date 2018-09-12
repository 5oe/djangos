from django.forms import ModelForm
from repository.models import *
from django.forms.widgets import Textarea, SelectMultiple


class ModelInfoForm(ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'


class SettingHandler(object):
    def __init__(self, model):
        self.model = model

    def get_fields(self):
        if self.model == UserInfo:
            fields = [
                'email', 'username', 'password', 'role', 'is_active',
                'is_staff', 'user_permissions', 'groups'
            ]
        else:
            fields = '__all__'
        return fields

    def get_help_text(self):
        help_texts = {}
        if self.model == UserInfo:
            help_texts = {
                'password': """
                    原始密码不存储,所以没有办法看到
                    这个用户的密码,但是你可以改变密码 
                    使用 <a href='javascript:;' tag-href='password/?popup=1' onclick="PopUpWindow(this.getAttribute('tag-href'))">修改密码</a>.
                             """
            }
        return help_texts

    def get_exclude_fields(self):
        # if self.model == UserInfo:
        #     return ['password']
        return []


class FormClassFactory(object):
    @classmethod
    def from_admin(cls, admin, is_add=False):
        class Meta:
            model = admin.cls_info
            setting_handler = SettingHandler(model)
            fields = setting_handler.get_fields()
            help_texts = setting_handler.get_help_text()
            exclude = setting_handler.get_exclude_fields()
            if not is_add:
                exclude = admin.readonly_fields

        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                field_obj = cls.base_fields[field_name]
                if isinstance(field_obj.widget, Textarea):
                    field_obj.widget.attrs.update({'cols': '70', 'rows': '13'})
                if isinstance(field_obj.widget, SelectMultiple):
                    field_obj.widget.attrs.update({'style': 'width:380px;height:270px'})

                if Meta.model == UserInfo:
                    cls.base_fields['password'].disabled = True

            return ModelForm.__new__(cls)

        form_cls = type('DynamicModelForm', (ModelForm,), {'Meta': Meta, '__new__': __new__})
        return form_cls
