from api.home import bp
from flask import redirect, render_template
from flask_login import login_required, current_user

@bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)