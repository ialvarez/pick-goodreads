from flask import Flask, url_for, redirect, make_response, request, render_template
from rauth.service import OAuth1Service, OAuth1Session
from xml.parsers.expat import ExpatError
from random import choice
import xmltodict
import json

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


def get(path, params=None):
    session = OAuth1Session(
                consumer_key=KEY,
                consumer_secret=SECRET,
                access_token=request.cookies.get('access_token'),
                access_token_secret=request.cookies.get('access_token_secret'))

    if not params:
        params = {}

    base = "http://www.goodreads.com/"
    resp = session.get(base + path, params=params)

    try:
        return xmltodict.parse(resp.content)['GoodreadsResponse']
    except ExpatError:
        return 500


@app.route('/')
def homepage():
    me = get('api/auth_user')
    if me == 500:
        user = 'Anonymous'
    else:
        user = me['user']['name']
    return render_template('home.html', user=me['user']['name'])


@app.route('/shelf')
def shelf():
    me = get('api/auth_user')
    data = get('review/list/%s.xml' % me['user']['@id'], params={
            'v':2,
            'shelf': 'to-read',
        })
    review = choice(data['reviews']['review'])
    print review['id']
    print review['book']['id']['#text']
    print review['book']['text_reviews_count']['#text']
    print review['book']['title']
    print review['book']['large_image_url']
    print review['book']['small_image_url']
    print review['book']['image_url']
    print review['book']['average_rating']
    print review['url']
    print '\n'

    return 'ok'

@app.route('/login')
def login():
    token, secret = goodreads.get_request_token(header_auth=True)
    resp = make_response(redirect(goodreads.get_authorize_url(token)))
    resp.set_cookie('request_token', token)
    resp.set_cookie('request_secret', secret)
    return resp


@app.route('/oauth_authorized')
def oauth_authorized():
    request_token = request.cookies.get('request_token')
    request_secret = request.cookies.get('request_secret')
    session = goodreads.get_auth_session(request_token, request_secret)
    resp = make_response(redirect('/'))
    resp.set_cookie('access_token', session.access_token)
    resp.set_cookie('access_token_secret', session.access_token_secret)
    return resp


if __name__ == "__main__":
    app.run(port=65011)
