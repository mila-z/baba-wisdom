from api.wisdom import bp
from api.models import Wisdom
from flask import jsonify, render_template, request, flash
from flask_login import current_user, login_required
import json
from api import db

@bp.route('/daily-wisdom')
@login_required
def daily_wisdom():
    return render_template('daily_wisdom.html', user=current_user)

@bp.route('/wisdom-from-the-past-day')
@login_required
def wisdom_from_the_past_day():
    return render_template('wisdom_past_day.html', user=current_user)

@bp.route('/post-wisdom', methods=['GET', 'POST'])
@login_required
def post_wisdom():
    if request.method == 'POST':
        wisdom_text = request.form.get('wisdom_text')
        age_input = request.form.get('age_restriction')
        age_restriction = int(age_input) if age_input and age_input.isdigit() else 0

        if len(wisdom_text) < 1:
            flash('Note is too short!', category='error')
        else:
            new_wisdom = Wisdom(
                text=wisdom_text, 
                baba_id=current_user.id, 
                age_restriction=age_restriction
            )
            db.session.add(new_wisdom)
            db.session.commit()
            flash('Wisdom added!', category='success')

    return render_template('post_wisdom.html', user=current_user)

@bp.route('/view-wisdom', methods=['GET', 'POST'])
@login_required
def view_wisdom():
    wisdom = Wisdom.query.filter_by(baba_id=current_user.baba.id).all()
    return render_template('view_wisdom.html', user=current_user, wisdoms=wisdom)

@bp.route('/delete-wisdom', methods=['DELETE'])
@login_required
def delete_wisdom():
    data = request.get_json()
    wisdom_id = data.get('wisdom')

    wisdom = Wisdom.quesry.get(wisdom_id)
    if wisdom and wisdom.baba_id == current_user.id:
        db.session.delete(wisdom)
        db.session.commit()

    return jsonify({})
