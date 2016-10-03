Python-Refract
==============

A Python 2/3 library for interacting with
`Refract elements <https://github.com/refractproject/refract-spec>`_.

Install from Git
----------------

.. code-block:: bash

    pip install git+htts://github.com/joshbenner/python-refract.git#egg=refract

Usage
-----

Create refract structures from native data:

.. code-block:: python

    >>> ns = refract.Namespace()
    >>> array_element = ns.element([1, 2, 3])
    >>> array_element.refracted
    {
      "content": [
        {
          "content": 1,
          "attributes": {},
          "meta": {},
          "element": "number"
        },
        {
          "content": 2,
          "attributes": {},
          "meta": {},
          "element": "number"
        },
        {
          "content": 3,
          "attributes": {},
          "meta": {},
          "element": "number"
        }
      ],
      "attributes": {},
      "meta": {},
      "element": "array"
    }
