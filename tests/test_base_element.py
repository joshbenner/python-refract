from refract import Element, Namespace
from refract.elements import ElementMap


def test_element_map_create():
    em = ElementMap(Namespace(), foo='bar')
    assert em['foo'].native_value == 'bar'


def test_element_init_meta():
    el = Element(
        meta=dict(
            id='foobar',
            # classes=('a', 'b'),
            title='Title',
            description='Description'
        ),
        namespace=Namespace()
    )
    assert el.meta['id'].native_value == 'foobar'
    # assert el.meta['classes'].value == ('a', 'b')
    assert el.meta['title'].native_value == 'Title'
    assert el.meta['description'].native_value == 'Description'


def test_element_init_value():
    el = Element('')
    assert el.native_value == ''


def test_element_init_attributes():
    el = Element(attributes={'foo': 'bar'}, namespace=Namespace())
    assert el.attributes['foo'].native_value == 'bar'


def test_element_repr():
    el = Element('foo', namespace=Namespace())
    assert repr(el) == "<Element: 'foo'>"


def test_element_set_value():
    el = Element('foo', namespace=Namespace())
    el.set_content('bar')
    assert el.native_value == 'bar'


def test_element_refracted():
    el = Element('foo', meta={'id': 'foo'}, attributes={'bar': 'baz'},
                 namespace=Namespace())
    assert el.refracted == {
        'element': 'element',
        'meta': {
            'id': 'foo'
        },
        'attributes': {
            'bar': 'baz'
        },
        'content': 'foo'
    }


def test_element_equals():
    el = Element('foo', namespace=Namespace())
    assert el.equals('foo')
    assert not el.equals('bar')


def test_element_clone():
    el = Element({'foo': 'bar'}, {'id': 'test'}, namespace=Namespace())
    el2 = el.clone()
    assert id(el) != id(el2)

    # Value change
    assert el.native_value == el2.native_value
    el.native_value['foo'] = 'baz'
    assert el.native_value != el2.native_value

    # Meta change
    assert el.meta['id'].equals(el2.meta['id'].native_value)
    el.meta['id'] = 'test2'
    assert not el.meta['id'].equals(el2.meta['id'].native_value)


