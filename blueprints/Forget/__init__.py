from flask import Blueprint


Forgot_bp = Blueprint('Forgot', __name__, url_prefix='/Forgot')


from . import routes
