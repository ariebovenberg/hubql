from pathlib import Path

import pytest

import hubql
import quiz

_ = quiz.selector

TOKEN = Path('~/.snug/github_token.txt').expanduser().read_text().strip()


@pytest.fixture(scope='session')
def execute():
    return hubql.executor(TOKEN)


def test_module():
    issubclass(hubql.Issue, quiz.Object)


def test_simple(execute):

    query = hubql.query(
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
            ]
        ]
    )

    result = execute(query)
    assert 'errors' not in result
