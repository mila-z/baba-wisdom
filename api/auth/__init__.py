"""
Initialize the athentication package.

This file defines the authentication blueprint and registers its routes.
"""
from flask import Blueprint

bp = Blueprint('auth', __name__)

from api.auth import routes
