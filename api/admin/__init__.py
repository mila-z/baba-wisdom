"""
Initialize the admin package.

This file defines the admin blueprint and registers its routes.
"""
from flask import Blueprint
from api.admin import routes

bp = Blueprint('admin', __name__)
