"""GraphQL client for the GitHub v4 API. Experimental.

It serves mainly as an example of using
the `quiz <https://quiz.readthedocs.io/>`_ GraphQL client.
"""
from functools import partial
from pathlib import Path

import snug

import quiz

__author__ = 'Arie Bovenberg'
__copyright__ = 'Arie Bovenberg, 2018'
__version__ = '0.0.1'

URL = "https://api.github.com/graphql"
_SCHEMA_PATH = Path(__file__).parent / 'schema.json'


def auth_factory(auth):
    if isinstance(auth, str):
        return snug.header_adder({'Authorization': f'bearer {auth}'})
    else:
        assert isinstance(auth, tuple)
        return auth


schema = quiz.Schema.from_path(_SCHEMA_PATH, module=__name__)
schema.populate_module()
query = schema.query


def execute(obj, auth, url=URL, **kwargs):
    return quiz.execute(obj, auth=auth_factory(auth), url=url, **kwargs)


def execute_async(obj, auth, url=URL, **kwargs):
    return quiz.execute_async(obj, auth=auth_factory(auth), url=url, **kwargs)


executor = partial(partial, execute)
async_executor = partial(partial, execute_async)
