from flask import Blueprint

airQuality_bp = Blueprint('airQuality', __name__, url_prefix='/airQuality', template_folder='templates')

from . import routes