from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def user_login(request):
    if request.method == 'GET':
        return render(request, 'account/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        verify_code = request.POST.get('verify_code')
        remember = request.POST.get('remember')
        standard_verify_code = request.session.get('verify_code')

        user = authenticate(email=username, password=password)
        if not user:
            error_msg = '用户名或密码错误'
            return render(request, 'account/login.html', {'error_msg': error_msg})

        if standard_verify_code.upper() != verify_code.upper():
            error_msg = '验证码错误'
            return render(request, 'account/login.html', {'error_msg': error_msg})

        login(request, user)
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
            return HttpResponse('/account')


def user_logout(request):
    logout(request)
    return redirect('/account/login')


def user_register(request):
    from form.account.user import UserCreationForm
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'account/register.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        verify_code = request.POST.get('verify_code')
        standard_verify_code = request.session.get('verify_code')
        if form.is_valid():
            if standard_verify_code.upper() != verify_code.upper():
                form.add_error(None, '验证码错误')
                return render(request, 'account/register.html', {'form': form})
            form.save()
            return HttpResponse('成功')
        else:
            return render(request, 'account/register.html', {'form': form})


@login_required
def change_password(request):
    from form.account.user import PasswordChangeForm
    if request.method == 'GET':
        form = PasswordChangeForm
        return render(request, 'account/change-password.html', {'form': form})
    elif request.method == 'POST':
        form = PasswordChangeForm(data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password1']
            user = request.user
            user.set_password(new_password)
            return HttpResponse('成功')
        else:
            return render(request, 'account/change-password.html', {'form': form})


def create_verify_code(request):
    from io import BytesIO
    from utils import check_code
    buffer = BytesIO()
    img, code = check_code.create_validate_code()
    img.save(buffer, 'PNG')
    request.session['verify_code'] = code
    return HttpResponse(buffer.getvalue())
