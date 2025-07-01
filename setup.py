import os
from glob import glob
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

#  rm -R build/ dist/ *egg-info
#  python3 setup.py sdist
#  twine upload dist/*

SRC_FOLDER = 'src'
PKG_NAME = 'django_spid_cie_sp'

setup(
    name=PKG_NAME,
    version='1.0.0',
    packages=[PKG_NAME],
    package_dir={PKG_NAME: f"{SRC_FOLDER}/{PKG_NAME}"},
    package_data={PKG_NAME: [i.replace(f'{SRC_FOLDER}/{PKG_NAME}/', '')
                                   for i in glob(f'{SRC_FOLDER}/{PKG_NAME}/**',
                                                 recursive=True)]
    },
    license='Apache License 2.0',
    description="Rende il tuo progetto Django un Service Provider SAML2 per l'autenticazione con SPID e CIE",
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/francesco-filicetti/django-spid-cie-sp',
    author='Francesco Filicetti',
    author_email='francesco.filicetti@unical.it',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'djangosaml2',
        'design-django-theme'
    ],
)
