import abc
import copy
import types
from collections import MutableSequence, MutableMapping, OrderedDict

import six

__all__ = ['Element', 'NullElement', 'BooleanElement', 'NumberElement',
           'StringElement', 'ArrayElement', 'ObjectElement', 'MemberElement']


class ElementMap(MutableMapping, dict):
    namespace = None

    def __init__(self, namespace, **kwargs):
        super(ElementMap, self).__init__()
        self.namespace = namespace
        self.update(kwargs)

    def __setitem__(self, key, value):
        value = self.namespace.element(value)
        dict.__setitem__(self, key, value)

    __getitem__ = dict.__getitem__
    __delitem__ = dict.__delitem__
    __iter__ = dict.__iter__
    __len__ = dict.__len__
    __contains__ = dict.__contains__


class Element(six.with_metaclass(abc.ABCMeta, object)):
    """
    Base element class

    :cvar element: The element name
    :cvar native_types: Optional tuple of Python types acceptable for element
    :cvar default_value: Default value for element if none is given
    :cvar scalar: Whether this element wraps scalar values. Determines if type
        rules are applied to content passed into constructor.
    """
    element = 'element'
    native_types = None
    default_value = None
    scalar = True

    def __init__(self, content=None, meta=None, attributes=None,
                 namespace=None):
        """
        :param content: Content to be wrapped by this Element
        :type content: any

        :param meta: Metadata
        :type meta: dict

        :param attributes: Attributes
        :type attributes: dict

        :param namespace: Namespace this Element is a part of
        :type namespace: refract.Namespace
        """
        self._content = None
        self.namespace = namespace
        self.set_content(self.default_value if content is None else content)
        self.meta = ElementMap(namespace, **(meta or {}))
        self.attributes = ElementMap(namespace, **(attributes or {}))

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__,
                                 repr(self.native_value))

    @property
    def content(self):
        return self._content

    @property
    def native_value(self):
        """
        The native Python value wrapped by this Element.
        """
        return self.content

    def _require_native_type(self, value):
        if self.native_types is not None:
            if not isinstance(value, self.native_types):
                cls = self.__class__.__name__
                names = ', '.join(t.__name__ for t in self.native_types)
                raise ValueError('{} content may be: {}'.format(cls, names))

    def set_content(self, value):
        """
        Set the wrapped value.
        """
        self._require_native_type(value)
        self._content = value

    @property
    def refracted(self):
        """
        The serialized Refract data for this Element

        :rtype: dict
        """
        return {
            'element': self.element,
            'meta': self._refracted_keyvals(self.meta),
            'attributes': self._refracted_keyvals(self.attributes),
            'content': self.content
        }

    @staticmethod
    def _should_refract(element):
        """
        Determine if an element should be refracted.

        If not, caller can use the simple value instead of a refract structure.

        An element should be refracted if:
        - It is a member element
        - It has any meta data or attributes

        :param element: The element to evaluate.
        :type element: Element

        :rtype: bool
        """
        return (element.element == 'member' or
                element.meta.keys() or
                element.attributes.keys())

    def _refracted_keyvals(self, keyvals):
        """
        Refracts the contents of all values for given key/val pairs.

        :param keyvals: Pairs to refract
        :type keyvals: dict[str, Element]

        :rtype: dict[str, dict]
        """
        return {k: v.refracted if self._should_refract(v) else v.native_value
                for k, v in six.iteritems(keyvals)}

    @classmethod
    def from_refract(cls, doc, namespace):
        return cls(doc['content'], doc['meta'], doc['attributes'], namespace)

    def equals(self, value):
        """
        Check if the wrapped value is equivalent to the provided value.

        :param value: The value to compare

        :rtype: bool
        """
        return value == self.native_value

    def clone(self):
        """
        Obtain a cloned of this Element

        :return: New element with identical data
        """
        return self.__class__(
            copy.deepcopy(self.content),
            copy.deepcopy(self.meta),
            copy.deepcopy(self.attributes),
            self.namespace
        )


class NullElement(Element):
    element = 'null'
    native_types = (types.NoneType,)


class BooleanElement(Element):
    element = 'boolean'
    native_types = (bool,)
    default_value = False


class NumberElement(Element):
    element = 'number'
    native_types = (int, float)
    default_value = 0


class StringElement(Element):
    element = 'string'
    native_types = six.string_types
    default_value = ''

    @property
    def length(self):
        return len(self.content)


class ArrayElement(Element, MutableSequence, list):
    element = 'array'
    native_types = (tuple, list, set)
    default_value = []

    def __setitem__(self, index, value):
        list.__setitem__(self, index, self.namespace.element(value))

    __getitem__ = list.__getitem__
    __delitem__ = list.__delitem__
    __len__ = list.__len__

    def insert(self, index, value):
        list.insert(self, index, self.namespace.element(value))

    @property
    def content(self):
        return self[0:]  # Full slice as efficient copy

    def set_content(self, value):
        self._require_native_type(value)
        self[:] = [self.namespace.element(v) for v in value]

    @property
    def native_value(self):
        return [item.native_value for item in self]

    @property
    def refracted(self):
        refracted = super(ArrayElement, self).refracted
        refracted['content'] = [item.refracted for item in self]
        return refracted


class MemberElement(Element):
    element = 'member'
    default_value = (None, None)
    native_types = (tuple, dict)
    scalar = False

    _key = None
    _value = None

    def set_content(self, value):
        self._require_native_type(value)
        if len(value) != 2:
            raise ValueError('MemberElement values are two-element tuples')
        self.key, self.value = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = self.namespace.element(value)

    @property
    def content(self):
        return self.key, self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.namespace.element(value)

    @property
    def native_value(self):
        return {
            'key': self.key.native_value,
            'value': self.value.native_value
        }

    @property
    def refracted(self):
        refracted = super(MemberElement, self).refracted
        refracted['content'] = {
            'key': self.key.refracted,
            'value': self.value.refracted
        }
        return refracted

    @classmethod
    def from_refract(cls, doc, namespace):
        raise NotImplementedError  # Only loads as part of ObjectElement


class ObjectElement(Element, MutableMapping):
    """
    Object Element imlpementing the array[Member Element] schema.
    """
    element = 'object'
    native_types = (dict,)
    default_value = {}

    def __iter__(self):
        for member in self.content:
            yield member.key.native_value

    def __setitem__(self, key, value):
        existing = self.get(key)
        if existing is None:
            self._content.append(MemberElement((key, value),
                                               namespace=self.namespace))
        else:
            existing.value = value

    def __len__(self):
        return len(self._content)

    def __getitem__(self, key):
        for member in self._content:
            if member.key.native_value == key:
                return member
        raise KeyError

    def __delitem__(self, key):
        for index, member in enumerate(self._content):
            if member.key.native_value == key:
                self._content.pop(index)
                return
        raise KeyError

    def set_content(self, value):
        self._require_native_type(value)
        self._content = [MemberElement((k, v), namespace=self.namespace)
                         for k, v in six.iteritems(value)]

    @property
    def native_value(self):
        return {m.key.native_value: m.value.native_value for m in self.content}

    @property
    def refracted(self):
        refracted = super(ObjectElement, self).refracted
        refracted['content'] = [m.refracted for m in self._content]
        return refracted

    @classmethod
    def from_refract(cls, doc, namespace):
        parse = namespace.from_refract
        # Content populates to a list, so keeping order is less surprising.
        content = OrderedDict(
            (parse(m['content']['key']), parse(m['content']['value']))
            for m in doc['content'])
        return cls(content, doc['meta'], doc['attributes'], namespace)
