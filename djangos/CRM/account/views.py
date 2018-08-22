from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def user_login(request):
    if request.method == 'GET':
        return render(request, 'account/login.htm')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)  # 注意不要和自己定义的函数名冲突
            remember = request.POST.get('remember')
            if remember:
                # 设置三十天有效
                request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                # 浏览器关闭时自动失效
                request.session.set_expiry(0)

            pre_url = request.GET.get('next')
            if pre_url:
                return redirect(pre_url)
            else:
                return redirect('/myAdmin')
        else:
            return render(request, 'account/login.htm', {'error_msg': "用户名或密码错误"})


def user_logout(request):
    logout(request)
    return redirect('/myAdmin')


