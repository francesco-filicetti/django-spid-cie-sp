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

def get_requirements(fname='requirements.txt'):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    fopen = open(fname, 'r')
    install_requirements = []
    dependency_links=[]
    packages = fopen.read().splitlines()
    for ir in packages:
        url = re.findall(regex, ir)
        install_requirements.append(ir) if not url \
        else dependency_links.append(url[0][0])
    return [install_requirements, dependency_links]
    
setup(
    name=PKG_NAME,
    version='1.0.0',
    packages=[PKG_NAME],
    package_dir={PKG_NAME: f"{SRC_FOLDER}/{PKG_NAME}"},
    package_data={PKG_NAME: [i.replace(f'{SRC_FOLDER}/{PKG_NAME}/', '')
                                   for i in glob(f'{SRC_FOLDER}/{PKG_NAME}/**',
                                                 recursive=True)]
    },
    license='3-clause BSD',
    description="Rende il tuo progetto Django un Service Provider SAML2 per l'autenticazione con SPID e CIE",
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/francesco-filicetti/django-spid-cie-sp',
    author='Francesco Filicetti',
    author_email='easyweb.wa@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=get_requirements()[0],
    dependency_links=get_requirements()[1],
)
