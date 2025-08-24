"""
Wisdom routes.

This module provides functionality for:
- Posting wisdom (Baba only)
- Viewing wisdom
- Daily and past-day wisdom
- Deleting wisdom
- Managing categories associated with wisdom
"""
from typing import List, Optional, Tuple
from datetime import date
import random
from sqlalchemy import func
from flask import jsonify, render_template, request, flash, redirect, url_for
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required
from api import db
from api.wisdom import bp
from api.models import Wisdom, Category

def get_age(birth_date: date, today: Optional[date] = None) -> int:
    """
    Compute the age of a person given a birth date.

    Args:
        birth_date (date): Birth date of the person.
        today (Optional[date]): Reference date to compute age. Defaults to today.

    Returns:
        int: Computed age.
    """
    if today is None:
        today = date.today()

    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

@bp.route('/wisdom-from-the-past-day')
@login_required
def wisdom_from_the_past_day() -> ResponseReturnValue:
    """
    Display wisdom posted today, filtered by age restriction for apprentices.

    Returns:
        ResponseReturnValue: Rendered template with today's wisdom.
    """
    date_today = date.today()
    query = Wisdom.query.where(func.date(Wisdom.posted) == date_today)
    if current_user.role == 'apprentice':
        age = get_age(current_user.apprentice.birth_date, date_today)
        print(age)
        query = query.where(Wisdom.age_restriction <= age)

    wisdom = query.all()
    return render_template('wisdom_past_day.html', user=current_user, wisdoms=wisdom)

def get_daily_wisdom() -> Optional[Wisdom]:
    """
    Return a single daily wisdom, randomized but consistent per day.

    Returns:
        Optional[Wisdom]: A random wisdom object, or None if none available.
    """
    all_wisdom: List[Wisdom] = Wisdom.query.where(Wisdom.age_restriction == 0).all()
    today_str = date.today().isoformat()

    random.seed(today_str)

    if all_wisdom:
        return random.choice(all_wisdom)
    return None

@bp.route('/daily-wisdom')
@login_required
def daily_wisdom() -> ResponseReturnValue:
    """
    Display a daily wisdom to the user.

    Returns:
        ResponseReturnValue: Rendered template with the daily wisdom.
    """
    return render_template('daily_wisdom.html', user=current_user, wisdom=get_daily_wisdom())

def add_categories(submitted: List[str]) -> List[Category]:
    """
    Add new categories.

    Args:
        submitted (List[str]): List of category names.

    Returns:
        List[Category]: List of Category objects corresponding to submitted names.
    """
    current = {c.name: c for c in Category.query.all()}
    category_objects: List[Category] = []

    for c_name in submitted:
        if c_name in current:
            category_objects.append(current[c_name])
        else:
            category = Category(name=c_name)
            db.session.add(category)
            db.session.flush()
            category_objects.append(category)

    return category_objects

@bp.route('/post-wisdom', methods=['GET', 'POST'])
@login_required
def post_wisdom() -> ResponseReturnValue:
    """
    Allow a Baba to post wisdom with optional categories and age restrictions.

    Returns:
        ResponseReturnValue: Rendered template ir redirect after posting a wisdom. 
    """
    if request.method == 'POST':
        if current_user.role != 'baba':
            flash('Only a baba can post wisdom!', category='errror')
            return redirect(url_for('home.home'))
        wisdom_text = request.form.get('wisdom_text')
        categories = request.form.get('categories')
        categories = [c.strip().lower() for c in categories.split(',')]
        age_input = request.form.get('age_restriction')
        age_restriction = int(age_input) if age_input and age_input.isdigit() else 0

        if len(wisdom_text) < 1:
            flash('Note is too short!', category='error')
        elif age_restriction < 0 or age_restriction > 122:
            flash('Age must be between 0 and 122!', category='error')
        else:
            new_wisdom = Wisdom(
                text=wisdom_text,
                baba_id=current_user.id,
                age_restriction=age_restriction
            )

            category_objects = add_categories(categories)
            new_wisdom.categories.extend(category_objects) 

            db.session.add(new_wisdom)
            db.session.commit()
            flash('Wisdom added!', category='success')

    return render_template('post_wisdom.html', user=current_user)

@bp.route('/view-wisdom', methods=['GET', 'POST'])
@login_required
def view_wisdom() -> ResponseReturnValue:
    """
    Display wisdom posted by the current Baba, or all wisdom for admin roles.

    Returns:
        ResponseReturnValue: Rendered template with wisdom list.
    """
    if current_user.role == 'apprentice':
        flash('Only a baba can view the wisdom she has posted!', category='error')
        return redirect(url_for('home.home'))
    elif current_user.role == 'baba':
        wisdom: List[Wisdom] = Wisdom.query.filter_by(baba_id=current_user.baba.id).all()
    else:
        wisdom: List[Wisdom] = Wisdom.query.all()
    return render_template('view_wisdom.html', user=current_user, wisdoms=wisdom)

@bp.route('/delete-wisdom', methods=['DELETE'])
@login_required
def delete_wisdom() -> Tuple[ResponseReturnValue, int]:
    """
    Delete a wisdom posted by the current Baba.

    Returns:
        tuple: JSON response with success or error message and HTTP status code.
    """
    if current_user.role == 'apprentice':
        return jsonify({'error': 'Only a baba can delete wisdom'}), 403

    data = request.get_json()
    wisdom_id = data.get('wisdomId')

    wisdom = Wisdom.query.get(wisdom_id)
    if wisdom and wisdom.baba_id == current_user.baba.id:
        db.session.delete(wisdom)
        db.session.commit()
        return jsonify({'success': True})

    return jsonify({'error': 'Wisdom not found or not yours'}), 404
