# TODO 验证层
from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import length, NumberRange, DataRequired  # DataRequired是不为空，即使是空格也不能


class SearchForm(Form):
    # 从名字就可以看出这个Form是为了验证Search这个视图函数的
    q = StringField(validators=[DataRequired(), length(min=1, max=30, message='长度不合要求'), ])
    page = IntegerField(validators=[NumberRange(min=1, max=99, message='大小不合要求'), ], default=1)
