from setuptools import setup, find_packages


setup(
    name='refract',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),

    description='Refract elements manipulation library',
    author='Joshua Benner',
    author_email='josh@bennerweb.com',
    license='MIT',

    install_requires=[
        'six'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov'
        ]
    }
)
