import pytest

from refract.namespace import Namespace, ElementClassNotFound
from refract.elements import *


def test_namespace_default():
    n = Namespace()
    assert len(n.element_classes) > 0
    assert isinstance(n.element(1), NumberElement)


def test_namespace_register():
    n = Namespace()

    class FooElement(Element):
        element = 'foo'

    n.register_element_class(FooElement)
    assert n.element_classes['foo'] == FooElement


def test_namespace_register_rename():
    n = Namespace()

    class FooElement(Element):
        element = 'foo'

    n.register_element_class(FooElement, name='bar')
    assert n.element_classes['bar'] == FooElement
    assert 'foo' not in n.element_classes


def test_namespace_detect():
    n = Namespace()

    class Foo(object):
        pass

    class FooElement(Element):
        element = 'foo'

    n.register_element_class(FooElement)
    n.add_detection(lambda v: isinstance(v, Foo), FooElement)

    assert n.detected_element_class(Foo()) == FooElement


def test_namespace_detect_prepend():
    n = Namespace()

    class FooElement(Element):
        element = 'foo'

    n.add_detection(lambda v: v is None, FooElement, prepend=True)
    assert n.detected_element_class(None) == FooElement


def test_namespace_unregister():
    n = Namespace()
    n.unregister_element_class('null')
    assert 'null' not in n.element_classes


def test_namespace_element_not_detected():
    n = Namespace(no_defaults=True)
    with pytest.raises(ElementClassNotFound):
        n.detected_element_class('foo')
