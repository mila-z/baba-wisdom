"""
Initialize the search package.

This file defines the search blueprint and registers its routes.
"""
from flask import Blueprint
from api.search import routes

bp = Blueprint('search', __name__)
