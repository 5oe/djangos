from django import forms
from django.forms import widgets
from django.forms import fields


class MyForm(forms.Form):
    user = fields.CharField(
        max_length=5,
        min_length=2,
        widget=widgets.TextInput(attrs={'id': 'i1', 'class': 'c1'})
    )

    gender = fields.ChoiceField(
        choices=((1, '男'), (2, '女'),),
        initial=2,
        widget=widgets.RadioSelect
    )

    city = fields.CharField(
        max_length=2,
        min_length=1,
        initial=2,
        widget=widgets.Select(choices=((1, '上海'), (2, '北京'),))
    )


if __name__ == '__main__':
    from DataCreator.libs.env import init

    init()
    a = {'user': 'abc', 'gender': 1}
    b = {'city': 'ab'}
    f = MyForm(a, b)
    if f.is_valid():
        print(dir(f))
    else:
        for k, v in f.errors.items():
            print(k, v.data)
