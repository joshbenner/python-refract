import pytest

from refract import BooleanElement


def test_boolean_element_name():
    assert BooleanElement().element == 'boolean'


def test_boolean_value():
    assert BooleanElement().native_value is False
    assert BooleanElement(True).native_value is True


def test_boolean_refracted():
    assert BooleanElement().refracted == {
        'element': 'boolean',
        'meta': {},
        'attributes': {},
        'content': False
    }
