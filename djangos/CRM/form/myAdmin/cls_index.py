from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError
from myAdmin import site


class ArgsForm(forms.Form):
    app = fields.CharField()
    cls = fields.CharField()

    def clean_app(self):
        app = self.cleaned_data.get('app')
        if site.is_app_in_register(app):
            return self.cleaned_data['app']
        else:
            raise ValidationError('app不存在')

    def clean_cls(self):
        app = self.cleaned_data.get('app')
        cls = self.cleaned_data.get('cls')
        if site.is_cls_in_register(app, cls):
            return self.cleaned_data['cls']
        else:
            raise ValidationError('cls不存在')
