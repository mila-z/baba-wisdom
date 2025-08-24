"""
Initialize the home package.

This file defines the home blueprint and registers its routes.
"""
from flask import Blueprint
from api.home import routes

bp = Blueprint('home', __name__)
