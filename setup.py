__author__ = 'seyriz'
"""
Flask-Naver
-----------

Oauth2 wraper for Naver login
"""

from setuptools import setup

setup(
    name='Flask-naver',
    version='1.0',
    url='http://github.com/seyriz/flask-naver',
    license='BSD',
    author='Han-Wool, Lee',
    author_email='kudnya@gmail.com',
    description='Oauth2 wraper for Naver login',
    long_description=__doc__,
    py_modules=['flask-naver'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['naver_login'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        "flask",
        "xml2dict",
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)