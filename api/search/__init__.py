from flask import Blueprint

bp = Blueprint('search', __name__)

from api.search import routes