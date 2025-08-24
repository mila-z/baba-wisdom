"""
Admin statistics routes.

This module provides routes for administators to view 
aggregated statistics about villages, stars, and categories.
All routes are restricted to admin users.
"""
from flask import render_template, redirect, url_for, flash
from flask.typing import ResponseReturnValue
from flask_login import login_required, current_user
from sqlalchemy import func, desc
from api.admin import bp
from api.models import Baba, Wisdom, Review, User, WisdomCategories, Category
from api import db

@bp.route('/village-statistics', methods=['GET', 'POST'])
@login_required
def village_statistics() -> ResponseReturnValue:
    """
    Display statistics about Babas grouped by village.

    Returns:
        ResponseReturnValue: Rendered HTML template showing
        village names and the number of Babas from each village,
        or a redirect if the user is not an admin.
    """
    if current_user.role != 'admin':
        flash('You have no access to this page!', category='error')
        return redirect(url_for('home.home'))
    results = (
        db.session.query(
            Baba.village,
            func.count(Baba.id).label('baba_count')
        )
        .group_by(Baba.village)
        .order_by(desc('baba_count'))
        .all()
    )
    return render_template(
        'village_statistics.html',
        user=current_user,
        results=results)

@bp.route('/star-statistics', methods=['GET', 'POST'])
@login_required
def star_statistics() -> ResponseReturnValue:
    """
    Display statistics about total stars for each Baba.

    Returns:
        ResponseReturnValue: Rendered HTML template showing
        usernames and the total number of stars recieved across
        their wisdom, or a redirect if the user is not an admin.
    """
    if current_user.role != 'admin':
        flash('You have no access to this page!', category='error')
        return redirect(url_for('home.home'))
    results = (
        db.session.query(
            User.username,
            func.sum(Review.num_stars).label('total_num_stars')
        )
        .join(Baba, Baba.user_id == User.id)
        .outerjoin(Wisdom, Wisdom.baba_id == Baba.id)
        .outerjoin(Review, Review.wisdom_id == Wisdom.id)
        .group_by(Baba.id)
        .order_by(desc('total_num_stars'))
        .all()
    )

    return render_template(
        'star_statistics.html',
        user=current_user,
        results=results
    )

@bp.route('/category-statistics', methods=['GET', 'POST'])
@login_required
def category_statstics() -> ResponseReturnValue:
    """
    Display statistics about wisdom categories.

    Returns:
        ResponseReturnValue: Rendered HTML template showing
        category names and the number of wisdoms in each, 
        or a redirect if the user is not an admin.
    """
    if current_user.role != 'admin':
        flash('You have no access to this page!', category='error')
        return redirect(url_for('home.home'))    
    results = (
        db.session.query(
            Category.name,
            func.count(WisdomCategories.wisdom_id).label('num_wisdom')
        )
        .join(WisdomCategories, Category.id == WisdomCategories.category_id)
        .group_by(Category.name)
        .order_by(desc('num_wisdom'))
        .all()
    )

    return render_template(
        'category_statistics.html',
        user=current_user,
        results=results
    )
