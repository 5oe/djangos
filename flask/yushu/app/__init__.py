from flask import Flask
from app.models.models import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    register_blueprint(app)

    # 数据库插件绑定app
    db.init_app(app)
    db.create_all(app=app)

    # 登录插件绑定app
    login_manager.init_app(app=app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录'

    # 邮件插件绑定app
    mail.init_app(app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
