from api.admin import bp
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from api.models import Baba, Wisdom, Review, User, WisdomCategories, Category
from api import db
from sqlalchemy import func, desc

@bp.route('/village-statistics', methods=['GET', 'POST'])
@login_required
def village_statistics():
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
    
    return render_template('village_statistics.html', user=current_user, results=results)

@bp.route('/star-statistics', methods=['GET', 'POST'])
@login_required
def star_statistics():
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

    return render_template('star_statistics.html', user=current_user, results=results)

@bp.route('/category-statistics', methods=['GET', 'POST'])
@login_required
def category_statstics():
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

    return render_template('category_statistics.html', user=current_user, results=results)