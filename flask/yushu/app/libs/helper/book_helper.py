from flask import current_app
from app.libs.tools.http_tool import HTTP


# class YuShuBook(object):
#     isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
#     keyword_url = 'http://t.yushu.im/v2/booksearch?q={}&count={}&start={}'
#     per_page = 15 # 这里应该写在配置文件里，因为需要更改时，在配置文件中更改远比在代码中更改好
#
#     @classmethod
#     def search_by_isbn(cls, isbn):
#         url = cls.isbn_url.format(isbn)
#         ret = HTTP.get(url)
#         return re# class YuShuBook(object):
#     isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
#     keyword_url = 'http://t.yushu.im/v2/booksearch?q={}&count={}&start={}'
#     per_page = 15 # 这里应该写在配置文件里，因为需要更改时，在配置文件中更改远比在代码中更改好
#
#     @classmethod
#     def search_by_isbn(cls, isbn):
#         url = cls.isbn_url.format(isbn)
#         ret = HTTP.get(url)
#         return ret
#
#     @classmethod
#     def search_by_keyword(cls, keyword, page=1):
#         url = cls.keyword_url.format(keyword, cls.per_page, (page - 1) * cls.per_page)
#         ret = HTTP.get(url)
#         return ret
#
#
#     # 在这个类中编写保存数据到数据库的办法
#     # 因为这是最接近我们得到数据的地方t
#
#     @classmethod
#     def search_by_keyword(cls, keyword, page=1):
#         url = cls.keyword_url.format(keyword, cls.per_page, (page - 1) * cls.per_page)
#         ret = HTTP.get(url)
#         return ret
#
#
#     # 在这个类中编写保存数据到数据库的办法
#     # 因为这是最接近我们得到数据的地方



# TODO 重构为真正的面向对象
# 既描述特征，又具有一定行为，并且还有一种朦胧的抽象美，不会具体到某一程度，方便以后原理性的改变。
# 但是没有完美的面向对象，例如若需要将底层请求机制改变为数据库，则类变量的那两条url就没必要存在
# 可是，他妈的写在哪里，配置文件其实不错！

class YuShuBook(object):
    # 职责：向API发送请求，并存储到对象内部
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/booksearch?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        data = HTTP.get(url)
        self.__fill_single(data)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'],
                                      self.calculate_start(page))
        data = HTTP.get(url)
        self.__fill_collection(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']

        # 在这个类中编写保存数据到数据库的办法
        # 因为这是最接近我们得到数据的地方

    @property
    def first(self):
        return self.books[0] if self.total else None
