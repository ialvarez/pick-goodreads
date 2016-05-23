from __future__ import division
from flask import Flask, redirect, make_response, request, render_template, \
                  url_for
from random import choice, randint
from rauth.service import OAuth1Service, OAuth1Session
import xmltodict
from xml.parsers.expat import ExpatError

KEY = 'LBSo8qxEflIrs8SRenUTQ'
SECRET = 'bX1mw68KW9Bcx4hiO0o1bQWZS8alX14tVRKEOKUiDTI'
USER_AGENT = 'pick goodreads'

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY,

goodreads = OAuth1Service(
    consumer_key=KEY,
    consumer_secret=SECRET,
    request_token_url='http://www.goodreads.com/oauth/request_token',
    authorize_url='http://www.goodreads.com/oauth/authorize',
    access_token_url='http://www.goodreads.com/oauth/access_token',
    base_url='http://www.goodreads.com/'
)

cookie_keys = ['token', 'secret', 'request_token', 'request_secret']

sort_options = ['title', 'author', 'cover', 'rating', 'year_pub', 'date_pub',
                'date_pub_edition', 'date_started', 'date_read', 'date_updated',
                'date_added', 'recommender', 'avg_rating', 'num_ratings',
                'review', 'read_count', 'votes', 'random', 'comments', 'notes',
                'isbn', 'isbn13', 'asin', 'num_pages', 'format', 'position',
                'shelves', 'owned', 'date_purchased', 'purchase_location',
                'condition']


def get_cookie(key):
    if key not in cookie_keys:
        return None
    return request.cookies.get(key)


def random_review(me):
    per_page = randint(10, 20)
    page = randint(1, 2)
    random_sort = choice(sort_options)
    data = get('review/list/%s.xml' % me['user']['@id'], params={
        'v': 2,
        'shelf': 'to-read',
        'per_page': per_page,
        'page': page,
        'sort': random_sort,
    })
    return choice(data['reviews']['review'])


def get(path, params={}):
    session = OAuth1Session(consumer_key=KEY,
                            consumer_secret=SECRET,
                            access_token=get_cookie('token'),
                            access_token_secret=get_cookie('secret'))

    base = "http://www.goodreads.com/"
    resp = session.get(base + path, params=params)

    try:
        return xmltodict.parse(resp.content)['GoodreadsResponse']
    except ExpatError:
        return None


@app.route('/')
def homepage():
    me = get('api/auth_user')
    user = me['user']['name'] if me else 'Anonymous'
    return render_template('home.html', user=user)


@app.route('/shelf')
def shelf():
    me = get('api/auth_user')

    if not me:
        return redirect(url_for('login'))

    review = random_review(me)
    return render_template('book.html', **{
        'url': review['book']['link'],
        'title': review['book']['title'],
        'authors': review['book']['authors']['author']['name'],
        'description': review['book']['description'],
        'img': review['book']['image_url'],
        'ratings_count': review['book']['ratings_count'],
        'rating': review['book']['average_rating'],
    })


@app.route('/login')
def login():
    token, secret = goodreads.get_request_token(header_auth=True)
    resp = make_response(redirect(goodreads.get_authorize_url(token)))
    resp.set_cookie('request_token', token)
    resp.set_cookie('request_secret', secret)
    return resp


@app.route('/oauth_authorized')
def oauth_authorized():
    session = goodreads.get_auth_session(get_cookie('request_token'),
                                         get_cookie('request_secret'))
    resp = make_response(redirect('/'))
    resp.set_cookie('token', session.access_token)
    resp.set_cookie('secret', session.access_token_secret)
    return resp


if __name__ == "__main__":
    app.run(port=65011)
