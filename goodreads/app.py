from __future__ import division

from flask import Blueprint
from flask import session
from flask import redirect
from flask import render_template

from . import Goodreads

app = Blueprint('goodreads', __name__)


def goodreads():
    token, secret = None, None
    if 'token' in session:
        token = session['token']
    if 'secret' in session:
        secret = session['secret']
    return Goodreads(token=token, secret=secret)


@app.route('/')
def index():
    me = goodreads().me
    user = me['user']['name'] if me else 'Anonymous'
    return render_template('home.html', user=user)


@app.route('/login')
def login():
    session['login_token'], session['login_secret'], url = goodreads().login()
    return redirect(url)


@app.route('/oauth_authorized')
def oauth_authorized():
    session['token'], session['secret'] = goodreads().auth(
        session['login_token'],
        session['login_secret']
    )
    return redirect('/')


@app.route('/shelf')
def shelf():
    review = goodreads().get_random_review()
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
