from pathlib import Path

import pytest

import hubql
import quiz

_ = quiz.SELECTOR

TOKEN = Path('~/.creds/github.txt').expanduser().read_text().strip()


@pytest.fixture(scope='session')
def execute():
    return hubql.executor(auth=TOKEN)


def test_module():
    issubclass(hubql.Issue, quiz.Object)


def test_simple(execute):

    query = hubql.query[
        _
        .rateLimit[
            _
            .remaining
            .resetAt
        ]
        .repository(owner='octocat', name='hello-world')[
            _
            .createdAt
        ]
        .organization(login='github')[
            _
            .location
            .members(first=10)[
                _.edges[
                    _.node[
                        _.id
                    ]
                ]
                ('count').totalCount
            ]
        ]
    ]

    result = execute(query)
    assert result.organization.members.count > 200
    assert isinstance(result.organization, hubql.Organization)


def test_get_schema():
    schema = quiz.Schema.from_url(hubql.URL, auth=hubql.auth_factory(TOKEN))
    assert isinstance(schema, quiz.Schema)
