# 从各个子模块导入蓝图实例
from .typhoonAlarm import typhoonAlarm_bp
from .Login import Login_bp
from .weather import Weather_bp
from .airQuality import airQuality_bp
from .Register import Register_bp
from .auth import auth_bp
# 可以在这里添加更多蓝图，例如：
# from .another_blueprint import another_blueprint_bp

# 使用 __all__ 以方便 main.py 导入时管理
__all__ = ['typhoonAlarm_bp', 'Login_bp', 'Weather_bp', 'airQuality_bp', 'Register_bp', 'auth_bp']
