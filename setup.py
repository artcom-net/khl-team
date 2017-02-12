import os

from setuptools import setup

import khl_team


def read(file):
    path = os.path.join(os.path.dirname(__file__), file)
    with open(path, 'r', encoding='UTF-8') as file_:
        return file_.read()


setup(
    name='khl-team',
    version=khl_team.__version__,
    packages=['khl_team'],
    url='https://github.com/artcom-net/khl-team',
    license='MIT',
    author='Artem Kustov',
    author_email='artem.kustov@artcom-net.ru',
    description='Interface for obtaining data about KHL teams',
    long_description=read('README.rst'),
    install_requires=['beautifulsoup4==4.5.3', 'icalendar==3.11.2'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities'
    ]
)
