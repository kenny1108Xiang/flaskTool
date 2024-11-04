from flask import Blueprint

Register_bp = Blueprint('Register', __name__, url_prefix='/Register')

from . import routes