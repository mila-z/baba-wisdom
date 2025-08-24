"""
Review routes.

This module provides functionality for viewing and posting reviews on wisdom:
- Display all reviews for a specific wisodm
- Allow apprentices to post a review
"""
from flask import render_template, request, flash, redirect, url_for
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required
from api import db
from api.models import Review
from api.review import bp

@bp.route('/wisdom-reviews/<int:wisdom_id>', methods=['GET', 'POST'])
@login_required
def wisdom_reviews(wisdom_id: int) -> ResponseReturnValue:
    """
    Display and handle reviews for a specific wisdom.

    GET:
        - Fetch all reviews associated with the given wisdom ID.
        - Render the wisdom_reviews template with the reviews.

    POST:
        - Only allows apprentices to post a review.
        - Validates review length and number of stars.
        - Adds a new Review to the database if validation passes.
        - Redirects back to the same wisdom review page after posting.

    Args:
        wisdom_id (int): The ID of the wisdom to display and review.

    Returns:
        ResponseReturnValue: Rendered template of redirect response.
    """
    if request.method == 'POST':
        if current_user.role == 'baba':
            flash('Only an apprentice can post a review!', category='error')
            return redirect(url_for('review.wisdom_reviews', wisdom_id=wisdom_id))

        review_text = request.form.get('review_text')
        stars_input = request.form.get('num_stars')
        num_stars = int(stars_input) if stars_input and stars_input.isdigit() else 0

        if len(review_text) < 4:
            flash('Review text is too short!', category='error')
        elif num_stars < 0 or num_stars > 5:
            flash('Number of stars must be between 0 and 5!', category='error')
        else:
            new_review = Review(
                text=review_text,
                num_stars=num_stars,
                wisdom_id=wisdom_id,
                apprentice_id=current_user.id
            )
            db.session.add(new_review)
            db.session.commit()
            flash('Review added!', category='success')
            return redirect(url_for('review.wisdom_reviews', wisdom_id=wisdom_id))
    reviews = Review.query.where(Review.wisdom_id == wisdom_id).all()
    return render_template('wisdom_reviews.html', user=current_user, reviews=reviews)
