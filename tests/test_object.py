from collections import OrderedDict

import pytest
import six

from refract import ObjectElement, Namespace


@pytest.fixture
def obj_native():
    # Order is important since we store as array and do order-sensitive compare.
    return OrderedDict((('foo', 'bar'), ('z', 1)))


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
    assert list(obj.keys()) == ['foo', 'z']


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
