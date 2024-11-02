from flask import Blueprint

typhoonAlarm_bp = Blueprint('typhoonAlarm', __name__, url_prefix='/typhoonAlarm')

from . import routes