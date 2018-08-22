import json
from flask import request, jsonify

from app.form.book import SearchForm
from app.libs.helper.book_helper import YuShuBook
from app.libs.tools.book_tool import is_isbn_or_key
from . import web

from app.view_models.book import BookSingleViewModel, BookCollectionViewModel


@web.route('/book/search')
def search():
    """
    以GET参数形式获取参数
    
    q : 普通关键字 or isbn
    page : 页码
    
    实例 : ?q=村上&page=2
    """
    # 验证层
    form = SearchForm(request.args)  # form验证的参数其实一个字典

    if form.validate():
        q = form.q.data
        q = q.strip()
        page = form.q.data

        # 开始判断q的类型
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        # view_model 层
        books = BookCollectionViewModel()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        return json.dumps(books, default=lambda o: o.__dict__)
    else:
        return jsonify(form.errors)
