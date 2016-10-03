from collections import namedtuple


import six

from .elements import *

ElementDetector = namedtuple('ElementDetector', 'test type')


class ElementClassNotFound(Exception):
    pass


class Namespace(object):
    def __init__(self, no_defaults=False):
        """
        :param no_defaults: Exclude default primitive Element types
        :type no_defaults: bool
        """
        self.element_classes = {}
        self.element_detection = []
        if not no_defaults:
            default_classes = (
                BooleanElement,
                NullElement,
                NumberElement,
                StringElement,
                ArrayElement,
                MemberElement,
                ObjectElement
            )
            for element_class in default_classes:
                self.register_element_class(element_class)
            self.add_detection(lambda v: v is None, NullElement)
            self.add_detection(lambda v: isinstance(v, bool), BooleanElement)
            self.add_detection(lambda v: isinstance(v, (int, float)),
                               NumberElement)
            self.add_detection(lambda v: isinstance(v, six.string_types),
                               StringElement)
            self.add_detection(lambda v: isinstance(v, (list, tuple, set)),
                               ArrayElement)
            self.add_detection(lambda v: isinstance(v, dict), ObjectElement)

    def register_element_class(self, element_class, name=None):
        """
        Register an element type in this namespace.

        :param element_class: The Element class to register
        :type element_class: Type[Element]

        :param name: An optional name override
        :type name: str
        """
        self.element_classes[name or element_class.element] = element_class

    def unregister_element_class(self, name):
        """
        Remove an element type from this namespace.

        :param name: Name of the element type to remove
        :type name: str
        """
        del self.element_classes[name]

    def add_detection(self, func, element_class, prepend=False):
        """
        Add a new detection function used to determine element type for a value.

        :param func: Callable returning bool if value matches provided type
        :type func: callable

        :param element_class: Element class
        :type element_class: Type[Element]

        :param prepend: Whether to put this at the front of detection functions
        :type: bool
        """
        detector = ElementDetector(func, element_class)
        if prepend:
            self.element_detection.insert(0, detector)
        else:
            self.element_detection.append(detector)

    def element(self, value):
        """
        Given a value, return the appropriate Element wrapping it.

        :param value: Any value that can be described by this namespace
        :type value: Any

        :return: Element wrapping the value
        :rtype: Element
        """
        if isinstance(value, Element):
            return value
        element_class = self.detected_element_class(value)
        return element_class(value, namespace=self)

    def detected_element_class(self, value):
        """
        Detect which element class can wrap the given value

        :param value: The value whose Element class to detect
        :type value: Any

        :return: The Element class detected
        :rtype: Type[Element]

        :raises ElementClassNotFound: When no appropriate element class found
        """
        for detector in self.element_detection:  # type: ElementDetector
            if detector.test(value):
                return detector.type
        raise ElementClassNotFound

    def from_refract(self, doc):
        cls = self.element_classes[doc['element']]
        return cls.from_refract(doc, self)
