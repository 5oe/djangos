from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, desc, func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
# 用户验证插件，可以将用户到信息写入到cookie,但是需要模型类定义指定方法
# 如果不想定义，可以继承UserMinxin
# 注意：如果不是用id代表身份，即使是继承类UserMinxin，也要覆写get_id，返回代表标志用户的唯一凭证
from flask_login import UserMixin

from app.libs.helper.book_helper import YuShuBook

db = SQLAlchemy()


class BaseInfo(db.Model):
    __abstract__ = True
    # __abstract__是告诉sqlAlchemy不要创建这个表，使得这个表仅仅作为基类被继承即可
    isDelete = Column(Boolean, default=False)
    create_time = Column(Integer)

    def __init__(self):
        # 使用构造函数初始化，赋予对象初始属性，而不是用default参数
        self.create_time = int(datetime.now().timestamp())


class BookInfo(BaseInfo):
    __tablename__ = 'BookInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未命名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), unique=True)
    summary = Column(String(1000))
    image = Column(String(50))


class UserInfo(BaseInfo, UserMixin):
    __tablename__ = 'UserInfo'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    _password = Column('password', String(64))
    email = Column(String(50), unique=True)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50), nullable=True)
    wx_name = Column(String(32), nullable=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, password):
        return True if self.password == password else False

        # def get_id(self):
        #     return self.id


class User2Book(BaseInfo):
    __tablename__ = 'User2Book'
    id = Column(Integer, primary_key=True)
    # 用户外键
    # user = relationship('UserInfo')
    user_id = Column('user_id', Integer, ForeignKey('UserInfo.id'))
    # 书外键
    # book = relationship('BookInfo')
    # book_id = Column('book_id', Integer, ForeignKey('BookInfo.id'))
    isbn = Column(String(15), unique=True)

    launched = Column(Boolean, default=False)  # True表示要捐赠，False表示索要

    @classmethod
    def get_user_gifts(cls, user_id):
        gifts = User2Book.query.filter_by(user_id=user_id, launched=False). \
            order_by(desc(User2Book.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        # 计算心愿清单书中,每一本书的心愿请求数目
        # 使用isbn_list表的in查询
        # db.session.query 查询要指定具体的表,跨模型可以使用这个
        # filter使用的是条件表达式
        db.session.query(func.count(User2Book.id),User2Book.isbn).filter(User2Book.launched == False, \
                                                          User2Book.isDelete == False, \
                                                          User2Book.isbn.in_(isbn_list)). \
            group_by(User2Book.isbn).all()
        pass

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        # 链式调用 主体 Query
        # first() all()
        # 一个礼物里面有取多个礼物的方法，确实不合理，所以变为类方法
        recent_gift = User2Book.query.filter(launched=False). \
            group_by(User2Book.isbn).order_by(desc(User2Book.create_time)). \
            limit(30).distinct().all()
        return recent_gift


from app import login_manager


# 这个函数,flask-login 为了验证是否登录状态而定义的
# 返回一个user对象

@login_manager.user_loader
def get_user(user_id):
    return UserInfo.query.get(id=user_id)
