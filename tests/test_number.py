import pytest

from refract import NumberElement


def test_number_element_name():
    assert NumberElement().element == 'number'


def test_number_value():
    assert NumberElement(5).native_value == 5


def test_number_default_value():
    assert NumberElement().native_value == 0


def test_number_require_type():
    with pytest.raises(ValueError):
        NumberElement('foo')
