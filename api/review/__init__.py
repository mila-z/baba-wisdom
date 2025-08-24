"""
Initialize the review package.

This file defines the review blueprint and registers its routes.
"""
from flask import Blueprint
from api.review import routes

bp = Blueprint('review', __name__)
