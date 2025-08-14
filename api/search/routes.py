from api.search import bp
from flask import render_template
from flask_login import current_user

@bp.route('/search')
def search():
    return render_template('search_wisdom.html', user=current_user)
