from io import BytesIO
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Q  # 不等于
from django.core.urlresolvers import reverse
from web.forms import account
from responsitory.models import *
from utils import check_code
from utils import pagination


# Create your views here.


# def login(request):
#     '''
#     forms验证版，验证都在forms里面做了，但是因为读取数据库次数多，不考虑
#     :param request:
#     :return:
#     '''
#     if request.method == 'GET':
#         form = account.LoginForm(request=request)
#         context = {'form': form}
#         return render(request, 'web/user-login.html', context)
#     elif request.method == 'POST':
#         form = account.LoginForm(request=request, data=request.POST)
#         if form.is_valid():
#             return redirect('/backend/success')
#         else:
#             return render(request, 'web/user-login.html', {'form': form})


def login(request):
    if request.method == 'GET':
        form = account.LoginForm(request=request)
        context = {'form': form}
        return render(request, 'web/user-login.html', context)
    elif request.method == "POST":
        form = account.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            users = UsrInfo.objects.filter(username=username, password=password)
            if len(users) == 0:
                form.errors['username'] = ['用户名不存在或者密码错误', ]
                print(dict(form.errors))
                return render(request, 'web/user-login.html', {'form': form})
            else:
                user = users.values('id', 'username', 'password', 'email', 'phone', 'img', ).first()
                print(user)
                request.session['user'] = user
                # 判断是否有自动登录选项
                if form.cleaned_data.get('auto'):
                    request.session.set_expiry(60 * 60 * 24 * 30)
                return redirect('/backend/success')
        else:
            return render(request, 'web/user-login.html', {'form': form})


def login_out(request):
    request.session.clear()
    return redirect('/')


def register_check_username(request):
    username = request.GET.get('username', '')
    res = UsrInfo.objects.filter(username=username)
    if len(res) == 0:
        return JsonResponse({'res': True})
    else:
        return JsonResponse({'res': False})


def create_verify_code(request):
    buffer = BytesIO()
    img, code = check_code.create_validate_code()
    img.save(buffer, 'PNG')
    request.session['verify_code'] = code
    return HttpResponse(buffer.getvalue())


def register(request):
    if request.method == 'GET':
        form = account.RegiseterForm(request=request)
        context = {'form': form}
        return render(request, 'web/user-register.html', context)
    elif request.method == 'POST':
        form = account.RegiseterForm(request=request, data=request.POST)
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            conditions = {'username': username, 'password': password, 'email': email, 'phone': phone}

            u = UsrInfo.objects.create(**conditions)
            u.save()
            return redirect('/backend/success')
        else:
            # d = dict(form.errors)
            # print(d)
            context = {'form': form}
            return render(request, 'web/user-register.html', context)


def fregister(request):
    if request.method == 'GET':
        form = account.RegiseterForm(request)
        context = {'form': form}
        return render(request, 'web/user-register-f.html', context)

    elif request.method == 'POST':
        form = account.RegiseterForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            conditions = {'username': username, 'password': password, 'email': email, 'phone': phone}
            u = UsrInfo.objects.create(**conditions)
            u.save()
            return redirect('/backend/success')
        else:
            context = {'form': form}
            return render(request, 'web/user-register-f.html', context)


def test(request):
    form = account.TestForm(request)
    context = {'form': form}
    return render(request, 'test.html', context)


def index(request, **kwargs):
    # 获得按点赞数排行的点赞对象集合
    # kwargs: {'index_kind': '2'}
    # 命名正则会使命名名字为参数传入视图 index_kind=2
    best_list = EvaluateInfo.objects.filter(action=1).values('article'). \
                    annotate(c=Count('article')).order_by('-c')[0:6]
    bests = []
    for obj in best_list:
        bests.append(ArticleInfo.objects.get(id=obj['article']))

    # 获得按评论数排行
    # 排除评论对象为评论，即父文章外键为空的评论对象
    comment_list = CommentInfo.objects.filter(~Q(article=None)). \
                       values('article').annotate(c=Count('article')).order_by('-c')[0:6]
    # print(comment_list.query)
    talks = []
    for obj in comment_list:
        talks.append(ArticleInfo.objects.get(id=obj['article']))

    # 获得显示的全部文章，按点击数排行
    # articles = ArticleInfo.objects.all().order_by('-read')
    if kwargs:
        base_url = reverse('index', kwargs=kwargs)
    else:
        base_url = '/'
    # 分页
    data_count = ArticleInfo.objects.filter(**kwargs).count()
    p = request.GET.get('p')
    page_obj = pagination.Pagination(p, data_count)
    article_list = ArticleInfo.objects.filter(**kwargs).order_by('-read')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)
    context = {
        'articles': article_list,
        'bests': bests,
        'talks': talks,
        'title': '首页',
        'page_str': page_str,
    }
    return render(request, 'web/index.html', context)


def blog(request, **kwargs):
    surfix = kwargs['surfix']
    # 首先判断，若没有这个博客，让他滚回首页
    blog = BlogInfo.objects.filter(surfix=surfix).select_related('user').first()
    if not blog:
        return redirect('/')

    # 看看url是不是带条件的（类型2）
    condition = kwargs.get('condition', '')
    p = request.GET.get('p')

    if condition != '':
        # url带有条件
        if condition == 'tag':
            article_count = Article2Tag.objects.filter(tag_id=int(kwargs['value'])).count()
            page = pagination.Pagination(p, article_count, per_page_count=3)
            # 多表链接查询，只要有关系便可以使用
            articles = ArticleInfo.objects.filter(article2tag__tag_id=int(kwargs['value']))
        elif condition == 'type':
            article_count = ArticleInfo.objects.filter(category_id=int(kwargs['value']), blog=blog).count()
            page = pagination.Pagination(p, article_count, per_page_count=3)
            articles = ArticleInfo.objects.filter(category_id=int(kwargs['value']), blog=blog). \
                           order_by('-time')[page.start:page.end]
        elif condition == 'date':
            article_count = ArticleInfo.objects.filter(blog=blog). \
                extra(where=['date_format(time,"%%Y-%%m")=%s'], params=[kwargs['value'], ]).count()
            page = pagination.Pagination(p, article_count, per_page_count=3)
            articles = ArticleInfo.objects.filter(blog=blog). \
                           extra(where=['date_format(time,"%%Y-%%m")=%s'], params=[kwargs['value'], ]). \
                           order_by('-time')[page.start:page.end]
    else:
        # 没带条件，获取全部文章
        article_count = ArticleInfo.objects.filter(blog=blog).count()
        page = pagination.Pagination(p, article_count, per_page_count=3)
        articles = ArticleInfo.objects.filter(blog=blog).order_by('time')[page.start:page.end]

    base_url = request.path
    page_str = page.page_str(base_url)

    # 以下是共有的数据
    # 获得标签
    tags = TagInfo.objects.filter(blog=blog)

    # 获得个人类型
    kinds = KindInfo.objects.filter(blog=blog)

    # 获得统计日期
    date_list = ArticleInfo.objects.distinct_date(blog=blog)
    date_list = sorted(list(date_list))
    # date_list ['2017-6','2018-6']
    dates = []
    for obj in date_list:
        # c = ArticleInfo.objects.filter(blog=blog, time__year=l[0], time__month=l[1]).count()
        # 上面的查询语句不知道为什么使用time__month就查不出任何东西
        c = ArticleInfo.objects.filter(blog=blog).extra(
            where=['date_format(time,"%%Y-%%m")=%s'], params=[obj, ]).count()
        dates.append((obj, c))

    # 粉丝数
    fans_count = Star2Fans.objects.filter(star_user=blog.user).count()
    # 关注数
    star_count = Star2Fans.objects.filter(fans_user=blog.user).count()

    return render(request, 'web/blog.html', locals())


def blog_article(request, surfix, article_id):
    blog = BlogInfo.objects.filter(surfix=surfix).select_related('user').first()
    if not blog:
        return redirect('/')
    # 获得标签
    tags = TagInfo.objects.filter(blog=blog)

    # 获得个人类型
    kinds = KindInfo.objects.filter(blog=blog)

    # 获得统计日期
    date_list = ArticleInfo.objects.distinct_date(blog=blog)
    date_list = sorted(list(date_list))
    # date_list ['2017-6','2018-6']
    dates = []
    for obj in date_list:
        # c = ArticleInfo.objects.filter(blog=blog, time__year=l[0], time__month=l[1]).count()
        # 上面的查询语句不知道为什么使用time__month就查不出任何东西
        c = ArticleInfo.objects.filter(blog=blog).extra(
            where=['date_format(time,"%%Y-%%m")=%s'], params=[obj, ]).count()
        dates.append((obj, c))

    # 粉丝数
    fans_count = Star2Fans.objects.filter(star_user=blog.user).count()
    # 关注数
    star_count = Star2Fans.objects.filter(fans_user=blog.user).count()

    # 获得具体文章
    try:
        article = ArticleInfo.objects.get(id=article_id)
    except ArticleInfo.DoesNotExist:
        return redirect('/' + surfix + '/' + article_id)

    # 获得文章的全部评论,加上分页
    comment_count = CommentInfo.objects.filter(article=article).count()
    p = request.GET.get('p')
    page = pagination.Pagination(p, comment_count, per_page_count=5)
    comment_list = CommentInfo.objects.filter(article=article). \
                       select_related('comment_parent').order_by('time')[page.start:page.end]
    page_str = page.page_str()

    return render(request, 'web/blog-article.html', locals())


def page_handler(request, surfix, article_id):
    p = request.GET.get('p')
    try:
        article = ArticleInfo.objects.get(id=article_id)
    except ArticleInfo.DoesNotExist:
        return JsonResponse({'error': '文章不存在'})

    comment_count = CommentInfo.objects.filter(article=article).count()
    page = pagination.Pagination(p, comment_count, per_page_count=5)
    comment_list = CommentInfo.objects.filter(article=article). \
                       select_related('comment_parent').order_by('time')[page.start:page.end]
    comment_list = list(comment_list)
    res = []
    for obj in comment_list:
        if obj.comment_parent:
            comment_parent_username = obj.comment_parent.user.username
        else:
            comment_parent_username = None
        tmp = {
            'id': obj.id,
            'time': obj.time.strftime('%Y年-%m月-%d日 %H:%M'),
            'username': obj.user.username,
            'detail': obj.detail,
            'comment_parent_username': comment_parent_username,
        }
        res.append(tmp)

    return JsonResponse(res, safe=False)
