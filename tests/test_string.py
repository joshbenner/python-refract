import pytest

from refract import StringElement


def test_string_element_name():
    assert StringElement().element == 'string'


def test_string_default_value():
    assert StringElement().native_value == ''


def test_string_require_type():
    with pytest.raises(ValueError):
        StringElement(5)


def test_string_length():
    assert StringElement('foo').length == 3
