from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError
from myAdmin import site


class AppArgsForm(forms.Form):
    app = fields.CharField()

    def clean_app(self):
        app = self.cleaned_data.get('app')
        if site.is_app_in_register(app):
            return self.cleaned_data['app']
        else:
            raise ValidationError('app不存在')


class AppClsArgsForm(AppArgsForm):
    # app = fields.CharField()
    cls = fields.CharField()

    # def clean_app(self):
    #     app = self.cleaned_data.get('app')
    #     if site.is_app_in_register(app):
    #         return self.cleaned_data['app']
    #     else:
    #         raise ValidationError('app不存在')

    def clean_cls(self):
        app = self.cleaned_data.get('app')
        cls = self.cleaned_data.get('cls')
        if site.is_cls_in_register(app, cls):
            return self.cleaned_data['cls']
        else:
            raise ValidationError('cls不存在')


class AppClsObjArgsForm(AppClsArgsForm):
    id = fields.CharField()

    def clean_id(self):
        app = self.cleaned_data.get('app')
        cls = self.cleaned_data.get('cls')
        id = self.cleaned_data.get('id')
        cls_info = site.get_model(app_name=app, cls_name=cls)
        try:
            cls_info.objects.get(id=int(id))
        except cls_info.DoesNotExist:
            raise ValidationError('对象不存在')

        return self.cleaned_data['id']
