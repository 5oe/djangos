from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from repository.models.user import UserInfo
from django.forms import widgets


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}), \
                                max_length=32, min_length=8)
    password2 = forms.CharField(label='重复密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserInfo
        fields = ('email', 'username')
        labels = {
            'username': '用户名',
            'email': '邮箱',
        }
        error_messages = {
            '__all__': {},

            'email': {
                'required': '邮箱不能为空',
                'invalid': '邮箱格式错误',
            },
            'username': {
                'required': '用户名不能为空',
                'invalid': '用户名格式错误..',
            }
        }

        widgets = {
            'username': widgets.TextInput(attrs={'class': 'form-control'}),
            'email': widgets.TextInput(attrs={'class': 'form-control'})
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码输入不一致")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label='password',
                                         help_text=("原始密码不存储,所以没有办法看到"
                                                    "这个用户的密码,但是你可以改变密码 "
                                                    "使用 <a href=\"../password/\">修改密码</a>."))

    class Meta:
        model = UserInfo
        fields = ('email', 'password', 'username', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


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
