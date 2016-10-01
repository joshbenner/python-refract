import functools

import pytest
import six

from refract import *


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


def test_number_element_name():
    assert NumberElement().element == 'number'


def test_number_value():
    assert NumberElement(5).native_value == 5


def test_number_default_value():
    assert NumberElement().native_value == 0


def test_number_require_type():
    with pytest.raises(ValueError):
        NumberElement('foo')


def test_string_element_name():
    assert StringElement().element == 'string'


def test_string_default_value():
    assert StringElement().native_value == ''


def test_string_require_type():
    with pytest.raises(ValueError):
        StringElement(5)


def test_string_length():
    assert StringElement('foo').length == 3


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
    assert map(lambda e: e.native_value, array) == array_native


def test_array_filter(array, array_native):
    filtered = filter(lambda e: e.native_value, array)
    assert map(lambda e: e.native_value, filtered) == filter(None, array_native)


def test_array_reduce():
    numbers = ArrayElement([1, 2, 3, 4], namespace=Namespace())
    r = functools.reduce(lambda total, e: total + e.native_value, numbers, 0)
    assert r == 10


def test_array_insert(array, array_native):
    array.insert(0, 'foo')
    array_native.insert(0, 'foo')
    assert array.native_value == array_native


def test_member_native_value():
    me = MemberElement(('foo', 'bar'), namespace=Namespace())
    assert me.native_value == {'key': 'foo', 'value': 'bar'}


def test_member_bad_set_content():
    with pytest.raises(ValueError):
        MemberElement(('foo',))


@pytest.fixture
def obj_native():
    return {
        'foo': 'bar',
        'z': 1
    }


@pytest.fixture
def obj_refracted():
    return {
        'element': 'object',
        'meta': {},
        'attributes': {},
        'content': [
            {
                'element': 'member',
                'meta': {},
                'attributes': {},
                'content': {
                    'key': {
                        'element': 'string',
                        'meta': {},
                        'attributes': {},
                        'content': 'foo'
                    },
                    'value': {
                        'element': 'string',
                        'meta': {},
                        'attributes': {},
                        'content': 'bar'
                    }
                }
            },
            {
                'element': 'member',
                'meta': {},
                'attributes': {},
                'content': {
                    'key': {
                        'element': 'string',
                        'meta': {},
                        'attributes': {},
                        'content': 'z'
                    },
                    'value': {
                        'element': 'number',
                        'meta': {},
                        'attributes': {},
                        'content': 1
                    }
                }
            }
        ]
    }


@pytest.fixture
def obj(obj_native):
    return ObjectElement(obj_native, namespace=Namespace())


def test_object_element_name(obj):
    assert obj.element == 'object'


def test_object_default_value():
    assert ObjectElement().native_value == {}


def test_object_init_with_value(obj, obj_native):
    assert obj.native_value == obj_native


def test_object_set_new(obj, obj_native):
    obj['baz'] = 42
    obj_native['baz'] = 42
    assert obj.native_value == obj_native


def test_object_set_existing(obj, obj_native):
    obj['foo'] = True
    obj_native['foo'] = True
    assert obj.native_value == obj_native


def test_object_length(obj, obj_native):
    assert len(obj) == len(obj_native)


def test_object_get(obj, obj_native):
    assert obj['foo'].value.native_value == obj_native['foo']


def test_object_is_set(obj):
    assert 'foo' in obj


def test_object_del(obj):
    del obj['foo']
    assert 'foo' not in obj


def test_object_del_missing(obj):
    with pytest.raises(KeyError):
        del obj['baz']


def test_object_keys(obj):
    assert obj.keys() == ['foo', 'z']


def test_object_iter_keys(obj):
    assert [m for m in obj] == ['foo', 'z']


def test_object_iteritems(obj):
    assert [(i, m.value.native_value)
            for i, m in six.iteritems(obj)] == [('foo', 'bar'), ('z', 1)]


def test_object_refracted(obj, obj_refracted):
    assert obj.refracted == obj_refracted


def test_object_from_refracted(obj_refracted):
    obj = ObjectElement.from_refract(obj_refracted, Namespace())
    assert obj.refracted == obj_refracted
