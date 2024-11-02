from flask import Blueprint

Weather_bp = Blueprint('weather', __name__, url_prefix='/weather', static_folder='static', template_folder='templates')

from . import routes