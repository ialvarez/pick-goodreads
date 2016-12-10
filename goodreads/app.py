from __future__ import division

from flask import Blueprint
from flask import redirect
from flask import render_template

from . import Goodreads

app = Blueprint('goodreads', __name__)
goodreads = Goodreads()


@app.route('/')
def index():
    me = goodreads.get('api/auth_user')
    user = me['user']['name'] if me else 'Anonymous'
    return render_template('home.html', user=user)


@app.route('/login')
def login():
    token = goodreads.service_token
    return redirect(goodreads.service.get_authorize_url(token))


@app.route('/oauth_authorized')
def oauth_authorized():
    return redirect('/')


@app.route('/shelf')
def shelf():
    review = goodreads.get_random_review()
    if not review:
        return render_template('book.html')
    return render_template('book.html', **{
        'url': review['book']['link'],
        'title': review['book']['title'],
        'authors': review['book']['authors']['author']['name'],
        'description': review['book']['description'],
        'img': review['book']['image_url'],
        'ratings_count': review['book']['ratings_count'],
        'rating': review['book']['average_rating'],
    })
