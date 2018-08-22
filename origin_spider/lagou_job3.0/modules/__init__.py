import gevent
from gevent import monkey
from gevent.pool import Pool

monkey.patch_all()
from . import store, web_request, parse
from .log import logger

r = web_request.WebRequest()


def run(url, param_data, form_data):
    store.init_store_file()

    d = r.post(
        url=url,
        params=param_data,
        form_data=form_data
    )

    # 获得总页码
    if not d:
        logger.log(status=False, msg='获取页码失败')
        print('获取页码失败')
        return

    p = parse.Parse(d)

    jobs = []
    pool = Pool(5) #使用协程池，不然一下子发出100多个携程，就算机子可以，拉钩的反爬机制也不允许
    for i in range(1, p.page_num + 1):
        form_data['pn'] = i
        tmp_dict = dict()
        tmp_dict.update(form_data)
        jobs.append(pool.spawn(task, url, param_data, tmp_dict))
    print(jobs)
    gevent.joinall(jobs)


def process(d):
    # 解析
    p = parse.Parse(d)
    content = p.parse_content()

    # 存储
    store.store(content)


def task(url, param_data, form_data):
    response_dict = r.post(
        url=url,
        params=param_data,
        form_data=form_data
    )
    print(response_dict)
    if response_dict:
        process(response_dict)
    else:
        logger.log(status=False, msg='post提交失败')
        print('爬取失败')
