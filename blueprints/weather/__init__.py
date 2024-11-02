from flask import Blueprint

Weather_bp = Blueprint('weather', __name__, url_prefix='/weather', template_folder='templates')

from . import routes