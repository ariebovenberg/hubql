import datetime
import json
import sys
from functools import partial
from pathlib import Path

import snug

import quiz


_DEFAULT_URL = "https://api.github.com/graphql"
_SCHEMA_PATH = Path(__file__).parent / 'schema.json'

# uncomment to retrieve the lastest schema
# schema = execute(quiz.schema.get(_DEFAULT_URL))
# with _SCHEMA_PATH.open('w') as rfile:
#     schema = json.dump(schema, rfile)

with _SCHEMA_PATH.open('rt') as rfile:
    schema = json.load(rfile)


_SCALARS = {
    'URI':             str,
    'DateTime':        datetime.datetime,
    'HTML':            str,
    'GitObjectID':     str,
    'GitTimestamp':    str,
    'Date':            datetime.date,
    'X509Certificate': str,
    'GitSSHRemote':    str,
}

_CLASSES = quiz.types.gen(quiz.schema.load(schema), _SCALARS)


def bearer_auth(token):
    return snug.header_adder({'Authorization': f'bearer {token}'})


# TODO allow custom client set
def executor(token, url=_DEFAULT_URL, **kwargs):
    return quiz.executor(url=url, auth=bearer_auth(token), **kwargs)


query = partial(quiz.query, query_cls=_CLASSES['Query'])


# Add the classes to the module
__this = sys.modules[__name__]
for _name, _value in _CLASSES.items():
    setattr(__this, _name, _value)
