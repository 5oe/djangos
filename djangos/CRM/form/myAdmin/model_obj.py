from django.forms import ModelForm
from responsitory.models import *
from django.forms.widgets import Textarea, SelectMultiple


class ModelInfoForm(ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'


class FormClassFactory(object):
    @classmethod
    def from_admin(cls, admin, is_add=False):
        class Meta:
            model = admin.cls_info
            fields = '__all__'
            if not is_add:
                exclude = admin.readonly_fields

        def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                field_obj = cls.base_fields[field_name]
                if isinstance(field_obj.widget, Textarea):
                    field_obj.widget.attrs.update({'cols': '70', 'rows': '13'})
                # if isinstance(field_obj.widget, SelectMultiple):
                #     field_obj.widget.attrs.update({'style': 'width:380px;height:270px'})
            return ModelForm.__new__(cls)

        form_cls = type('DynamicModelForm', (ModelForm,), {'Meta': Meta, '__new__': __new__})
        return form_cls
