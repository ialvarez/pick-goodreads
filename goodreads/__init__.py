from instance.config import KEY
from instance.config import SECRET

from random import randint
from random import choice

from rauth.service import OAuth1Service
from rauth.service import OAuth1Session

from xmltodict import parse
from xml.parsers.expat import ExpatError


class Goodreads(object):
    def __init__(self, token=None, secret=None):
        self._service = None
        self._session = None
        self.token = token
        self.secret = secret

    @property
    def service(self):
        if not self._service:
            self._service = OAuth1Service(
                consumer_key=KEY,
                consumer_secret=SECRET,
                request_token_url='http://www.goodreads.com/oauth/request_token',
                authorize_url='http://www.goodreads.com/oauth/authorize',
                access_token_url='http://www.goodreads.com/oauth/access_token',
                base_url='http://www.goodreads.com/'
            )
        return self._service

    @property
    def session(self):
        if not self._session and self.token and self.secret:
            self._session = OAuth1Session(
                consumer_key=KEY,
                consumer_secret=SECRET,
                access_token=self.token,
                access_token_secret=self.secret
            )

        return self._session

    def login(self):
        params = {'header_auth': True}
        token, secret = self.service.get_request_token(**params)
        url = self.service.get_authorize_url(token)
        return token, secret, url

    def auth(self, token, secret):
        session = self.service.get_auth_session(token, secret)
        return session.access_token, session.access_token_secret

    def get(self, path, params={}):
        base = "http://www.goodreads.com/"
        try:
            resp = self.session.get(base + path, params=params)
            return parse(resp.content)['GoodreadsResponse']
        except AttributeError:
            return None
        except KeyError:
            return None
        except ExpatError:
            return None

    def get_random_review(self):
        me = self.get('api/auth_user')
        if not me:
            return None
        per_page = randint(10, 20)
        page = randint(1, 2)
        sort_options = ['title', 'author', 'cover', 'rating', 'year_pub', 'date_pub',
                        'date_pub_edition', 'date_started', 'date_read', 'date_updated',
                        'date_added', 'recommender', 'avg_rating', 'num_ratings',
                        'review', 'read_count', 'votes', 'random', 'comments', 'notes',
                        'isbn', 'isbn13', 'asin', 'num_pages', 'format', 'position',
                        'shelves', 'owned', 'date_purchased', 'purchase_location',
                        'condition']
        random_sort = choice(sort_options)
        data = self.get('review/list/%s.xml' % me['user']['@id'], params={
            'v': 2,
            'shelf': 'to-read',
            'per_page': per_page,
            'page': page,
            'sort': random_sort,
        })
        return choice(data['reviews']['review'])
