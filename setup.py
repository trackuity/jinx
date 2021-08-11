from setuptools import setup, find_packages


setup(
    name='jinx',
    version='0.2',
    license='Apache Software License (ASF)',
    description='Fast and simple indexing for JSON Lines files',
    url='https://github.com/trackuity/jinx',
    packages=find_packages(),
    install_requires=[
        'bsddb3==6.2.6',
        'Click==7.0',
        'Sanic==21.6.2',
        'ujson==1.35',
    ],
    entry_points='''
        [console_scripts]
        jinx=jinx.cli:cli
    ''',
)
