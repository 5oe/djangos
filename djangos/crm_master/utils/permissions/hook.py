# 这里主要用于GET参数过滤掉不适合的条件,默认的url可以访问所有带GET参数的
# 还要注意，用户的权限一般不会同时包括访问个体和访问全部

def visit_acquired_customer(request):
    # 只允许用户访问客户来源为qq群且已报名的客户
    # http://127.0.0.1:9000/ generalAdmin / repository / customer /?source = qq & status = signed
    if request.GET.get('source') == '0' and request.GET.get('contact') == '1':
        return True
    else:
        return False
