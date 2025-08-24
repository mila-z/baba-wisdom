"""
Home routes.

This module provides the homepage route, which requires
the user to be logged in and renders the home template.
"""
from flask import render_template
from flask.typing import ResponseReturnValue
from flask_login import login_required, current_user
from api.home import bp

@bp.route('/', methods=['GET', 'POST'])
@login_required
def home() -> ResponseReturnValue:
    """
    Render the homepage for the logged-in user.

    Returns:
        ResponseReturnValue: Rendered homepage remplate with the current user.
    """
    return render_template("home.html", user=current_user)
