from flask import Blueprint

bp = Blueprint('home', __name__)

from api.home import routes