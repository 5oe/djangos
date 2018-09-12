from django.forms import ModelForm
from django.forms import widgets
from repository.models import *
from django.forms.widgets import Textarea, SelectMultiple


class EnrollFormClassFactory(object):
    model = EnrollmentInfo

    def __form_new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})
            if isinstance(field_obj.widget, Textarea):
                field_obj.widget.attrs.update({'cols': '70', 'rows': '13'})
            if isinstance(field_obj.widget, SelectMultiple):
                field_obj.widget.attrs.update({'style': 'width:380px;height:270px'})

        return ModelForm.__new__(cls)

    @classmethod
    def from_base_info(cls, customer, consultant):
        class Meta:
            model = cls.model
            fields = ['customer', 'cls', 'consultant', ]
            widgets = {
                'customer': widgets.HiddenInput(
                    attrs={'value': customer.id}),
                'consultant': widgets.HiddenInput(
                    attrs={'value': consultant.id})
            }
            labels = {
                'customer': '',
                'consultant': '',
            }

        form_cls = type('DynamicModelForm', (ModelForm,), {'Meta': Meta, '__new__': cls.__form_new__})
        return form_cls
