import pytest

from refract import NullElement


def test_null_element_name():
    assert NullElement().element == 'null'


def test_null_value():
    assert NullElement().native_value is None


def test_null_refracted():
    refracted = NullElement().refracted
    assert refracted == {
        'element': 'null',
        'meta': {},
        'attributes': {},
        'content': None
    }


def test_null_cannot_set_nonnull():
    n = NullElement()
    with pytest.raises(ValueError):
        n.set_content('foo')
