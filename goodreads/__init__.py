from instance.config import KEY
from instance.config import SECRET

from json import dump

from random import randint
from random import choice

from rauth.service import OAuth1Service
from rauth.service import OAuth1Session

from xmltodict import parse

BASE_URL = 'http://www.goodreads.com'


class Goodreads(object):
    def __init__(self, token=None, secret=None):
        self._service = None
        self._session = None
        self._token = token
        self._secret = secret

        # me
        self._me = None

    @property
    def service(self):
        if not self._service:
            self._service = OAuth1Service(
                consumer_key=KEY,
                consumer_secret=SECRET,
                request_token_url='{}/oauth/request_token'.format(BASE_URL),
                authorize_url='{}/oauth/authorize'.format(BASE_URL),
                access_token_url='{}/oauth/access_token'.format(BASE_URL),
                base_url=BASE_URL
            )
        return self._service

    @property
    def session(self):
        if not self._session and self._token and self._secret:
            self._session = OAuth1Session(
                consumer_key=KEY,
                consumer_secret=SECRET,
                access_token=self._token,
                access_token_secret=self._secret
            )
        return self._session

    @property
    def me(self):
        if not self._me:
            self._me = self._get('/api/auth_user')
        return self._me

    def auth(self, token, secret):
        session = self.service.get_auth_session(token, secret)
        return session.access_token, session.access_token_secret

    def login(self):
        params = {'header_auth': True}
        token, secret = self.service.get_request_token(**params)
        url = self.service.get_authorize_url(token)
        return token, secret, url

    def _get(self, path, **params):
        url = BASE_URL + path
        goodreads_response = None
        if self.session:
            resp = self.session.get(url=url, **params)
            if resp.content:
                goodreads_response = parse(resp.content)['GoodreadsResponse']
                self._print(goodreads_response)
        return goodreads_response

    def _print(self, obj):
        with open('print.log', 'a') as f:
            dump(obj, f, indent=4)

    def get_random_review(self):
        if not self.me:
            return None
        per_page = randint(10, 20)
        page = randint(1, 2)
        sort_options = ['title', 'author', 'cover', 'rating', 'year_pub',
                        'date_pub', 'date_pub_edition', 'date_started',
                        'date_read', 'date_updated', 'date_added',
                        'recommender', 'avg_rating', 'num_ratings', 'review',
                        'read_count', 'votes', 'random', 'comments', 'notes',
                        'isbn', 'isbn13', 'asin', 'num_pages', 'format',
                        'position', 'shelves', 'owned', 'date_purchased',
                        'purchase_location', 'condition']
        random_sort = choice(sort_options)
        data = self._get('/review/list/%s.xml' % self.me['user']['@id'],
                         params={
                             'v': 2,
                             'shelf': 'to-read',
                             'per_page': per_page,
                             'page': page,
                             'sort': random_sort,
                         })
        return choice(data['reviews']['review'])
