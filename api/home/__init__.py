"""
Initialize the home package.

This file defines the home blueprint and registers its routes.
"""
from flask import Blueprint

bp = Blueprint('home', __name__)

from api.home import routes
