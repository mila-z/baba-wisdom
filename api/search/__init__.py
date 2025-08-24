"""
Initialize the search package.

This file defines the search blueprint and registers its routes.
"""
from flask import Blueprint

bp = Blueprint('search', __name__)

from api.search import routes
