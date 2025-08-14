from api.review import bp
from flask import render_template
from flask_login import current_user, login_required

@bp.route('/wisdom-reviews')
@login_required
def wisdom_reviews(wisdom_id):
    return render_template('wisdom_reviews.html', user=current_user)