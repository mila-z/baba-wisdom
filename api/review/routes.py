from api.review import bp
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from api.models import Review
from api import db

@bp.route('/wisdom-reviews/<int:wisdom_id>', methods=['GET', 'POST'])
@login_required
def wisdom_reviews(wisdom_id):
    if request.method == 'POST':
        if current_user.role == 'baba':
            flash('Only an apprentice can post a review!', category='error')
            return redirect(url_for('review.wisdom_reviews', wisdom_id=wisdom_id))

        review_text = request.form.get('review_text')
        stars_input = request.form.get('num_stars')
        num_stars = int(stars_input) if stars_input and stars_input.isdigit() else 0 #maybe make an exception of its not digits

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

# maybe add a delete review functionality