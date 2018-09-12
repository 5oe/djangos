from django import forms
from general_admin.form.cls_index import AppClsObjArgsForm
from repository.models import UserInfo


class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}), \
                                max_length=32, min_length=8)
    password2 = forms.CharField(label='重复密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码输入不一致")
        return password2


class PasswordArgsForm(AppClsObjArgsForm):
    def clean_cls(self):
        cls = super(PasswordArgsForm, self).clean_cls()
        if cls != UserInfo.__name__:
            raise forms.ValidationError('不存在password字段的model')
        else:
            return cls
