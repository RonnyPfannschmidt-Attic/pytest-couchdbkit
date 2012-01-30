from setuptools import setup
setup(
    name='pytest-couchdbkit',
    get_version_from_hg=True,

    description='py.test extension for per-test couchdb databases using couchdbkit',

    author='RonnyPfannschmidt',
    author_mail='ronny.pfannschmidt@gmx.de',

    requires=[
        'pytest',
        'couchdbkit',
    ],
    setup_requires=['hgdistver'],
)
