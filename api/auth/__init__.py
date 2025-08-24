"""
Initialize the athentication package.

This file defines the authentication blueprint and registers its routes.
"""
from flask import Blueprint
from api.auth import routes

bp = Blueprint('auth', __name__)
