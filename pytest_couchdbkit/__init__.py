import json
import pytest

from .dumper import dump_db
from .utils import server_from_config, dbname_from_config, \
        maybe_destroy_and_create

def pytest_addoption(parser):
    parser.addini('couchdbkit_backend', 'socketpool backend we should use', default='thread')
    parser.addini('couchdbkit_suffix', 'database name suffix')


def pytest_addhooks(pluginmanager):
    from . import hookspec
    pluginmanager.addhooks(hookspec)


def pytest_funcarg__couchdb_server(request):
    return server_from_config(request.config)



def pytest_funcarg__couchdb(request):
    server = request.getfuncargvalue('couchdb_server')
    tmpdir = request.getfuncargvalue('tmpdir')

    dbname = dbname_from_config(request.config, 'pytest_%s')
    db = maybe_destroy_and_create(server, dbname)


    def finalize_db():
        with tmpdir.join('couchdb.dump').open('w') as fp:
            dump_db(db, fp)
    request.addfinalizer(finalize_db)
    return db

