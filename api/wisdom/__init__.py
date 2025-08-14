from flask import Blueprint

bp = Blueprint('wisdom', __name__)

from api.wisdom import routes