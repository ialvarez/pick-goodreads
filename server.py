from flask import Flask, url_for, redirect, request, make_response
from rauth.service import OAuth1Service

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


@app.route('/')
def homepage():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    token, secret = goodreads.get_request_token(header_auth=True)
    resp = make_response(redirect(goodreads.get_authorize_url(token)))
    resp.set_cookie('token', token)
    resp.set_cookie('secret', secret)
    return resp


@app.route('/oauth_authorized')
def oauth_authorized():
    token, secret = request.cookies.get('token'), request.cookies.get('secret')
    gsession = goodreads.get_auth_session(token, secret)
    return gsession.get('%sapi/auth_user' % goodreads.base_url).text


if __name__ == "__main__":
    app.run(port=65011)
