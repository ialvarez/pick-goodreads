from flask import Flask, url_for, redirect
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
    # callback = url_for('goodreads_authorized', _external=True)
    # return goodreads.authorize(callback=callback, state=uuid.uuid4())
    request_token, _ = goodreads.get_request_token(header_auth=True)
    return '<a href="%s">Link</a>' % goodreads.get_authorize_url(request_token)


@app.route('/oauth_authorized')
def oauth_authorized():
    return 'Success'


if __name__ == '__main__':
    app.run(port=65011)