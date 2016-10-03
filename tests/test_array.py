import functools

import pytest

from refract import *


@pytest.fixture
def array_native():
    return ['a', True, None, 1]


@pytest.fixture
def array(array_native):
    return ArrayElement(array_native, namespace=Namespace())


def test_array_element_name(array):
    assert array.element == 'array'


def test_array_default_value():
    assert ArrayElement().native_value == []


def test_array_init_with_value(array, array_native):
    assert array.native_value == array_native


def test_array_set_value(array):
    array.set_content([2, 3])
    assert array.native_value == [2, 3]


def test_array_length(array):
    assert len(array) == 4


def test_array_refracted(array):
    assert array.refracted == {
        'element': 'array',
        'meta': {},
        'attributes': {},
        'content': [
            {
                'element': 'string',
                'meta': {},
                'attributes': {},
                'content': 'a'
            },
            {
                'element': 'boolean',
                'meta': {},
                'attributes': {},
                'content': True
            },
            {
                'element': 'null',
                'meta': {},
                'attributes': {},
                'content': None
            },
            {
                'element': 'number',
                'meta': {},
                'attributes': {},
                'content': 1
            }
        ]
    }


def test_array_set_native_value_for_index(array, array_native):
    array[0] = 42
    # Value changed
    assert array.native_value == [42] + array_native[1:]
    # Element type changed
    assert isinstance(array[0], NumberElement)


def test_array_get_element(array):
    assert array[1].element == 'boolean'


def test_array_get_value_for_index(array):
    assert array[0].native_value == 'a'


def test_array_iteration(array, array_native):
    assert [v.native_value for v in array] == array_native


def test_array_elements(array):
    assert isinstance(array[0], StringElement)
    assert isinstance(array[1], BooleanElement)
    assert isinstance(array[2], NullElement)
    assert isinstance(array[3], NumberElement)


def test_array_map(array, array_native):
    assert list(map(lambda e: e.native_value, array)) == array_native


def test_array_filter(array, array_native):
    filtered = filter(lambda e: e.native_value, array)
    native_value = list(map(lambda e: e.native_value, filtered))
    assert native_value == list(filter(None, array_native))


def test_array_reduce():
    numbers = ArrayElement([1, 2, 3, 4], namespace=Namespace())
    r = functools.reduce(lambda total, e: total + e.native_value, numbers, 0)
    assert r == 10


def test_array_insert(array, array_native):
    array.insert(0, 'foo')
    array_native.insert(0, 'foo')
    assert array.native_value == array_native


def test_array_delete(array, array_native):
    del array[0]
    del array_native[0]
    assert array.native_value == array_native
