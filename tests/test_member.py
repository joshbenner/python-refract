import pytest

from refract import MemberElement, Namespace


def test_member_native_value():
    me = MemberElement(('foo', 'bar'), namespace=Namespace())
    assert me.native_value == {'key': 'foo', 'value': 'bar'}


def test_member_bad_set_content():
    with pytest.raises(ValueError):
        MemberElement(('foo',))


def test_member_direct_from_refract():
    with pytest.raises(NotImplementedError):
        MemberElement.from_refract({}, Namespace())
