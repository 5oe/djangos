from twisted.internet import reactor  # 事件循环（终止条件，所有的socket都已经移除）
from twisted.web.client import getPage  # socket对象（如果下载完成，自动从时间循环中移除...）
from twisted.internet import defer  # defer.Deferred 特殊的socket对象 （不会发请求，手动移除


def response(content):
    print(content)


@defer.inlineCallbacks
def task():
    url = "http://www.baidu.com"
    d = getPage(url.encode('utf-8'))
    d.addCallback(response)
    yield d


def done(*args, **kwargs):
    reactor.stop()


d = task()
dd = defer.DeferredList([d, ])
dd.addBoth(done)

reactor.run()
