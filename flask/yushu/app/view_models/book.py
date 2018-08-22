class BookSingleViewModel(object):
    # 负责单一数据的数据的裁剪，并存储到对象内部，在构造方法内部进行即可
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = ' '.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.pages = book['pages']


class BookCollectionViewModel(object):
    def __init__(self):
        # 裁剪数据还有增加数据（keyword）
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookSingleViewModel(book) for book in yushu_book.books]
