from . import store, web_request, parse

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
        print('获取页码失败')
        return

    p = parse.Parse(d)
    for i in range(1, p.page_num + 1):
        form_data['pn'] = i
        response_dict = r.post(
            url=url,
            params=param_data,
            form_data=form_data
        )
        print(response_dict)
        if response_dict:
            process(response_dict)
        else:
            print('爬取失败')


def process(d):
    # 解析
    p = parse.Parse(d)
    content = p.parse_content()

    # 存储
    store.store(content)
