# -*- coding: utf-8 -*-
from setuptools import setup  # type: ignore

with open('README.rst', 'rt') as fh:
    long_description = fh.read()

setup(
    name='slmon',
    version='0.0.1',
    author='Stefan Valouch',
    author_email='svalouch@valouch.com',
    description='Extracts data from Solar-Log™ data loggers.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    project_urls={
        'Documentation': 'https://slmon.readthedocs.io/',
        'Source': 'https://github.com/svalouch/slmon/',
        'Tracker': 'https://github.com/svalouch/slmon/issues',
    },
    packages=['slmon'],
    package_data={'slmon': ['py.typed']},
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    url='https://github.com/svalouch/slmon/',
    python_requires='>=3.7',

    install_requires=[
        'click',
        'influxdb',
        'prometheus_client>=0.7',
        'pydantic>=1.2',
        'pyyaml',
        'requests>=2.21',
    ],
    extras_require={
        'dev': [
            'httpretty',
            'pytest',
            'pytest-cov',
            'pytest-pylint',
        ],
        'docs': [
            'Sphinx>=2.0',
            'sphinx-autodoc-typehints',
            'sphinx-rtd-theme',
            'sphinx-click',
        ],
        'postgres': [
            'psycopg2',
        ],
    },
    entry_points={
        'console_scripts': [
            'slmon=slmon.cli:cli',
        ],
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
