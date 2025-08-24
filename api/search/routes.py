"""
Search routes.

This module provides functionality for searching wisdom based on:
- Keywords in the wisdom text
- Categories associated with the wisdom
"""
from typing import List
from sqlalchemy import or_
from flask import render_template, request, flash, redirect, url_for
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required
from api.search import bp
from api.models import Wisdom, Category

@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search() -> ResponseReturnValue:
    """
    Handle searching wisdom by keywords and/or categories.

    GET:
        - Display the serach page with no results.

    POST:
        - Retrieve user input from fields 'categories' and 'keywords'.
        - Filter wisdom by the provided categories and keywords.
        - If no input is provided, flash an error and redirect back.
        - Return all matching wisdom.

    Returns:
        ResponseReturnValue: Rendered search page with search results. 
    """
    wisdom: List[Wisdom] = []

    if request.method == 'POST':
        query = Wisdom.query.outerjoin(Wisdom.categories)

        categories = request.form.get('categories')
        keywords = request.form.get('keywords')
        if categories is None and keywords is None:
            flash('You must have at least one input!', category='error')
            return redirect(url_for('search.search'))
        if categories:
            categories = [c.strip().lower() for c in categories.split(',')]
            query = query.filter(Category.name.in_(categories))
        if keywords:
            keywords = [k.strip() for k in keywords.split(',')]
            keyword_filters = [Wisdom.text.ilike(f"%{k}%") for k in keywords]
            query = query.filter(or_(*keyword_filters))
        wisdom = query.distinct().all()

    return render_template('search_wisdom.html', user=current_user, wisdoms=wisdom)
