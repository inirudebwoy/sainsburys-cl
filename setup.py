from os.path import join, dirname
from setuptools import setup


def read(fname):
    return open(join(dirname(__file__), fname)).read()

setup(
    name='sainsburys-cl',
    version='0.0.1',
    description=('Command line script that returns TODO'),
    long_description=open('README.md').read(),
    license='GPLv2',
    author='Michal Klich',
    author_email='michal@michalklich.com',
    include_package_data=True,
    packages=['sainsburys-cl'],
    url='https://github.com/inirudebwoy/sainsburys-cl',
    install_requires=read("requirements.txt"),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
