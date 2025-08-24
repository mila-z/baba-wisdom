"""
Initialize the wisdom package.

This file defines the wisdom blueprint and registers its routes.
"""
from flask import Blueprint

bp = Blueprint('wisdom', __name__)

from api.wisdom import routes