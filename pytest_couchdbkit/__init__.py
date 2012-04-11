import json
import pytest

from .dumper import dump_db

def pytest_addoption(parser):
    parser.addini('couchdbkit_backend', 'socketpool backend we should use', default='thread')
    parser.addini('couchdbkit_suffix', 'database name suffix')

def pytest_funcarg__couchdb_server(request):
    from couchdbkit import Server
    return Server(backend=request.config.getini('couchdbkit_backend'))

def pytest_funcarg__couchdb(request):
    server = request.getfuncargvalue('couchdb_server')
    tmpdir = request.getfuncargvalue('tmpdir')
    suffix = request.config.getini('couchdbkit_suffix')
    if not suffix:
        pytest.fail('no couchdbkit_suffix set in ini')
    dbname = 'pytest_' + suffix

    if dbname in server.all_dbs():
        server.delete_db(dbname)
    db = server.create_db(dbname)


    def finalize_db():
        with tmpdir.join('couchdb.dump').open('w') as fp:
            dump_db(db, fp)
    request.addfinalizer(finalize_db)
    return db

