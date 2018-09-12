from django.forms import ModelForm
from repository.models import CustomerInfo, EnrollmentInfo, CustomerDetailInfo
from django import forms
from django.forms import widgets


class EnrollmentForm(ModelForm):
    # agree = forms.CharField(
    #     label='同意协议',
    #     widget=widgets.CheckboxInput(attrs={'id': "is_agree", 'name': 'agree'}),
    #     required=False,
    # )

    def __new__(cls, *args, **kwargs):
        print("__new__", cls, args, kwargs)
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'form-control'})
            if field_name in cls.Meta.readonly_fields:
                filed_obj.widget.attrs.update({'disabled': 'true'})
                cls.base_fields[field_name].disabled = True
        return ModelForm.__new__(cls)

    class Meta:
        model = EnrollmentInfo
        fields = ['consultant', 'cls', ]
        readonly_fields = ['consultant']

    def clean(self):
        """
        防止恶意修改
        :return: 
        """
        if self.errors:
            raise forms.ValidationError(("Please fix errors before re-submit."))
        if self.instance.id is not None:  # means this is a change form ,should check the readonly fields
            for field in self.Meta.readonly_fields:
                old_field_val = getattr(self.instance, field)  # 数据库里的数据
                form_val = self.cleaned_data.get(field)
                if old_field_val != form_val:
                    self.add_error(field, "Readonly Field: field should be '{value}' ,not '{new_value}' ". \
                                   format(**{'value': old_field_val, 'new_value': form_val}))

    def save(self, commit=True):
        from datetime import datetime
        enrollment = super(EnrollmentForm, self).save(commit=False)
        enrollment.contract_agreed = True
        enrollment.contract_agreed_date = datetime.now()
        if commit:
            enrollment.save()
        return enrollment


class CustomerDetailForm(ModelForm):
    """
     name = models.CharField(max_length=8, verbose_name='真实姓名')
    identity_id = models.CharField(max_length=18, verbose_name='身份号码', unique=True)
    id_img_path = models.CharField(max_length=128, verbose_name='身份证照片路径', unique=True)
    passport_img_path = models.CharField(max_length=128, verbose_name='户口本照片路径', unique=True)
    birthday = models.DateField(verbose_name='出生日期')
    sex = models.SmallIntegerField(choices=[(0, '男'), (1, '女')], verbose_name='性别', default=0)
    phone = models.CharField(max_length=12, verbose_name='电话', unique=True)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    qq = models.CharField(max_length=16, verbose_name='qq账号', unique=True)
    wechar = models.CharField(max_length=32, verbose_name='微信号', null=True, blank=True, unique=True)
    work_status = models.SmallIntegerField(choices=[(0, '无业'), (1, '在职')], verbose_name='职业状态')
    place = models.CharField(max_length=32, verbose_name='居住地点')
    """

    class Meta:
        model = CustomerDetailInfo
        fields = '__all__'
        exclude = ['id_img_path', 'passport_img_path', 'contract']
        # widgets = {
        #     'id_img_path': widgets.HiddenInput(attrs={}),
        #     'passport_img_path': widgets.HiddenInput(attrs={})
        # }
        # labels = {
        #     'id_img_path': '',
        #     'passport_img_path': '',
        # }

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'form-control'})
        return ModelForm.__new__(cls)


class ImgForm(forms.Form):
    file = forms.ImageField()
