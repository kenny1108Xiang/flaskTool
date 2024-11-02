from flask import Blueprint

# 创建蓝图实例，名称为 'Login'
Login_bp = Blueprint('Login', __name__, url_prefix='/Login')

# 导入 routes.py 文件中的视图函数
from . import routes
