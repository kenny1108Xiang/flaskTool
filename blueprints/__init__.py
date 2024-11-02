# 从各个子模块导入蓝图实例
from .typhoonAlarm import typhoonAlarm_bp
from .Login import Login_bp
# 可以在这里添加更多蓝图，例如：
# from .another_blueprint import another_blueprint_bp

# 使用 __all__ 以方便 main.py 导入时管理
__all__ = ['typhoonAlarm_bp', 'Login_bp']
