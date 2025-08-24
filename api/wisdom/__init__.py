"""
Initialize the wisdom package.

This file defines the wisdom blueprint and registers its routes.
"""
from flask import Blueprint
from api.wisdom import routes

bp = Blueprint('wisdom', __name__)
