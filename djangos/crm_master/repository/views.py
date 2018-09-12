from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class EnterView(TemplateView):
    template_name = "enter.html"


class Teacher(View):  # 自定义的类必须继承View
    # 重写父类dispatch方法。程序定制时可以使用
    # 父类的dispatch方法，查找get、post等方法，基于反射实现的。
    def dispatch(self, request, *args, **kwargs):
        print("类似装饰器：before")
        print(*args, **kwargs)
        result = super(Teacher, self).dispatch(request, *args, **kwargs)
        print("类似装饰器：after")
        return result

    def get(self, request, *args, **kwargs):  # 定义get方法，get请求执行这个方法
        print(request.method)
        return render(request, 'myAdmin/enroll1.html')

    def post(self, request, *args, **kwargs):  # 定义post方法，post请求执行这个方法
        print(request.method, "post方式")
        return render(request, 'myAdmin/enroll1.html')


def student(request):
    return render(request, 'kingadmin/app_index.html')


def sale(request):
    return render(request, 'general_admin/child.html')


def news(request):
    from django.conf import settings
    from django.core.mail import EmailMessage
    from django.http import HttpResponse

    email_title = '邮件标题'
    email_body = """
    <img src="127.0.0.1:8000/account/create_verify_code" alt="验证码" height="40px" width="90px"
                                         class="verify-code">

    <a href="https://blog.csdn.net/xusongsong520/article/details/7966755">点击</a>                               
    """

    email = '363396239@qq.com'  # 对方的邮箱
    msg = EmailMessage(email_title, email_body, settings.EMAIL_HOST_USER, [email, ])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    return HttpResponse('ok')


def admin(request):
    pass


def boss(request):
    return render(request, 'crm/enrollment.html')
