# 1.利用getPage创建socket
# 2.将socket添加到事件循环中
# 3.开始事件循环（自动结束）

from twisted.internet import reactor   # 事件循环（终止条件，所有的socket都已经移除）
from twisted.web.client import getPage # socket对象（如果下载完成，自动从时间循环中移除...）
from twisted.internet import defer     # defer.Deferred 特殊的socket对象 （不会发请求，手动移除）


def response(content):
    print(content[:20])

@defer.inlineCallbacks
def task():
    url = "http://www.baidu.com"
    d1 = getPage(url.encode('utf-8'))
    d1.addCallback(response)
    a1 = yield d1
    print(a1)

    url = "http://www.baidu.com"
    d2 = getPage(url.encode('utf-8'))
    d2.addCallback(response)
    a2 = yield 1+1
    print(a2)

    url = "http://www.baidu.com"
    d3 = getPage(url.encode('utf-8'))
    d3.addCallback(response)
    a3 = yield d3
    print(a3)

    yield 1000

    yield defer.Deferred()

def done(*args,**kwargs):
    reactor.stop()

d=task()
print(d)
dd = defer.DeferredList([d,])
dd.addBoth(done)
reactor.run()