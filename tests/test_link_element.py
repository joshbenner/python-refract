import pytest

from refract import LinkElement, Namespace


@pytest.fixture
def link():
    link = LinkElement(namespace=Namespace())
    link.rel = 'foo'
    link.href = '/bar'
    return link


def test_link_creation(link):
    assert link.attributes['relation'].native_value == 'foo'
    assert link.attributes['href'].native_value == '/bar'


def test_link_convenience(link):
    assert link.rel == 'foo'
    assert link.relation == 'foo'
    assert link.href == '/bar'


def test_link_refract(link):
    assert link.refracted == {
        'element': 'link',
        'meta': {},
        'attributes': {
            'relation': 'foo',
            'href': '/bar'
        },
        'content': []
    }
