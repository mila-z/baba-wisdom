from flask import Blueprint

bp = Blueprint('review', __name__)

from api.review import routes