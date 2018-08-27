from django.forms import ModelForm
from responsitory.models import *


class ModelInfoForm(ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'


class FormClassFactory(object):
    @classmethod
    def from_admin(cls, admin):
        class Meta:
            model = admin.cls_info
            fields = '__all__'
            exclude = admin.readonly_fields

        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                field_obj = cls.base_fields[field_name]
                # field_obj.widget.attrs.update({'class': 'form-control'})
            return ModelForm.__new__(cls)

        form_cls = type('DynamicModelForm', (ModelForm,), {'Meta': Meta, '__new__': __new__})
        return form_cls
