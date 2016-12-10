from instance.config import KEY
from instance.config import SECRET

from random import randint
from random import choice

from rauth.service import OAuth1Service

from xmltodict import parse
from xml.parsers.expat import ExpatError


class Goodreads(object):
    def __init__(self):
        self._service = None
        self._service_token = None
        self._service_secret = None
        self._session = None

    @property
    def service_token(self):
        if not self._service_token:
            self._init_service_token_secret()
        return self._service_token

    @property
    def service_secret(self):
        if not self._service_secret:
            self._init_service_token_secret()
        return self._service_secret

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
        if not self._session:
            self._session = self.service.get_auth_session(self.service_token,
                                                          self.service_secret)
        return self._session

    def _init_service_token_secret(self):
        params = {'header_auth': True}
        self._service_token, self._service_secret = self.service.get_request_token(**params)

    def get(self, path, params={}):
        base = "http://www.goodreads.com/"
        try:
            resp = self.session.get(base + path, params=params)
            return parse(resp.content)['GoodreadsResponse']
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
