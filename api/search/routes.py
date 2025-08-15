from api.search import bp
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from api.models import Wisdom, Category
from sqlalchemy import or_

@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    wisdom = []

    if request.method == 'POST':
        query = Wisdom.query.outerjoin(Wisdom.categories)

        categories = request.form.get('categories')
        keywords = request.form.get('keywords')
        if categories is None and keywords is None:
            flash('You must have at least one input!', category='error')
            return redirect(url_for('search.search'))
        
        if categories:
            categories = [c.strip().lower() for c in categories.split(',')]
            query = query.filter(
                or_(
                    Category.name.in_(categories),
                    Category.id.is_(None))
            )
        
        if keywords:
            keywords = [k.strip() for k in keywords.split(',')]
            keyword_filters = [Wisdom.text.ilike(f"%{k}%") for k in keywords]
            query = query.filter(or_(*keyword_filters))
        
        wisdom = query.distinct().all()

    return render_template('search_wisdom.html', user=current_user, wisdoms=wisdom)
