from wtforms import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, length, Email, ValidationError
from app.models.models import UserInfo


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), length(8, 64), \
                                    Email(message='邮件格式不正确')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), \
                                         length(6, 32)])
    nickname = StringField(validators=[DataRequired(), \
                                       length(2, 10, message='用户名最少2个字符,最多10个字符')])

    # 单字段验证
    def validate_email(self, field):
        if UserInfo.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已经被注册')
