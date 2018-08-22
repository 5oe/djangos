from flask import Blueprint

web = Blueprint('web', __name__)  # 参数一蓝图名，参数二所在模块名
# 蓝图，用于在大型项目中分拆不同的文件
# 如果用蓝图方式注册，url_maps里注册endponts默认就不是单独的视图名称，而是'蓝图名称.视图名称'

from app.web import book
