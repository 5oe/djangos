from flask import Flask, render_template, request
from flask import template_rendered, request_started, request_finished, request_tearing_down, current_app
from flask import got_request_exception
from flask import current_app
from flask import appcontext_pushed, appcontext_popped

#
# from blinker import Namespace

app = Flask(__name__)


# 手动创建应用上下文
# with app.app_context():
#     print('*' * 20, current_app.name)


# signals = Namespace()
# index_called = signals.signal('index-called')


# ------------------------------
# 例子一
# template_reandered函数:当模版被渲染时触发信号函数
def print_template_rendered(sender, template, context, **extra):
    print('@' * 20)
    print('sender', sender, type(sender))
    print('template', template, type(template))
    print('context', context, type(context))
    print('extra', extra, type(extra))

    print(request.url)


# 将指定信号函数和应用以及信号事件（函数就是）
template_rendered.connect(print_template_rendered, app)


# ————————————————————————————————

# 例子二
# 与例子一样的效果,只不过使用装饰器简化代码来注册
@template_rendered.connect_via(app)
def with_template_rendered(sender, template, context, **extra):
    print('啊啊啊啊啊啊啊')
    sender.logger.debug('Template %s context:%s 啊啊啊啊啊' % (template.name, context))


# ————————————————————————————————————


###########################################
# 其他核心信号

# 所有请求收到就会触发,即使是404反问也是一样
@request_started.connect_via(app)
def with_request_started(sender, *args):
    # 这个信号发送于请求开始之前，且请求环境设置完成之后。
    # 因为请求环境已经绑定， 所以订阅者可以用标准的全局代理，如 request 来操作请求。
    print('请求开始时发送:')
    print(sender)
    print(args)


# 请求处理后发送，404也会发送，并且多一个response参数
@request_finished.connect_via(app)
def with_request_finished(sender, response, *args):
    print('请求结束后发送')
    print(response, type(response))
    print(sender)
    print(args)


# 发生异常时调用
@got_request_exception.connect_via(app)
def with_request_exception(sender, exception):
    print('发生异常了')
    print(sender, type(sender))
    print(exception, type(exception))


# 请求被销毁时发送，不管有无异常都会被发送。
# 但是我测试不出异常时被调用
@request_tearing_down.connect_via(app)
def with_request_tearing_down(sender, exc, *args):
    print('应用环境崩溃')
    print(sender, type(sender))
    print(exc, type(exc))


# 有两种方式来创建应用上下文。第一种是隐式的：无论何时当一个请求上下文被压栈时，
#  如果有必要的话一个应用上下文会被一起创建。由于这个原因，你可以忽略应用上下文的存在，除非你需要它
# http://docs.jinkan.org/docs/flask/appcontext.html
@appcontext_pushed.connect_via(app)
def with_appcontext_pushed(sender):
    print('应用上下文压入')


@appcontext_popped.connect_via(app)
def with_appcontext_poped(sender):
    print('应用上下文淡出')


# !!!!!!!!!!!!!!!!!!!!!
# 自定义信号

# 第一步，导入包，创建信号对象，以后用于装饰器
from blinker import Namespace

signals = Namespace()
mysign = signals.signal('mysign')


# 第二步,定义信号函数
@mysign.connect_via(app)
def with_mysign(sender, method, **extra):
    print('我的自定义我做主')
    print(method, type(method))  # method是请求方法的字符串,'GET'


@app.route('/')
def index():
    # 第三部：触发信号
    mysign.send(current_app._get_current_object(), method=request.method)
    return 'Hello Flask!ffffff'


@app.route('/test')
def test():
    a = 1 / 0
    return render_template('test.html')


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html')


# hook
########## Request Context Hook ##########
@app.before_request
def before_request():
    print('Hook: before_request')


@app.after_request
def after_request(response):
    print('Hook: after_request')
    return response


if __name__ == '__main__':
    app.run(debug=True)
