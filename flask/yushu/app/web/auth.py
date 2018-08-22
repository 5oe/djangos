from flask import render_template, redirect
from flask import request, flash
from flask_login import login_user, logout_user  # 写入用户id到cookie,需要用户模型类中定义get_id返回id
from flask_login import login_required, current_user  # current_user 代表当前访问网站用户模型对象
# 借由规定的函数定义出由id号获取取用户对象

from app.form.register import RegisterForm
from . import web
from app.models.models import UserInfo


@web.route('/login', method=['GET', 'POST'])
def login():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = UserInfo.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
        else:
            flash('账号不存在或者密码错误')
        return render_template('auth/login.html', form=form)


@web.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@web.route('/mygits')
@login_required
def my_gits():
    return 'pass'
