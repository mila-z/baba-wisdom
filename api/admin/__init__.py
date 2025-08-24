"""
Initialize the admin package.

This file defines the admin blueprint and registers its routes.
"""
from flask import Blueprint

bp = Blueprint('admin', __name__)

from api.admin import routes