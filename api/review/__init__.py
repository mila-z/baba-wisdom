"""
Initialize the review package.

This file defines the review blueprint and registers its routes.
"""
from flask import Blueprint

bp = Blueprint('review', __name__)

from api.review import routes
