import pytest_couchdbkit
from pytest_couchdbkit.utils import maybe_destroy_and_create
import couchdbkit
import mock

settings = {'couchdbkit_suffix': 'test', 'couchdbkit_backend': 'thread'}

def funcargs(name, request):
    if name == 'couchdb_server':
        return couchdbkit.Server()
    print 'get funcarg', name
    return getattr(request, name)

def pytest_funcarg__request(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    request = mock.MagicMock()
    request.config.getini.side_effect = settings.get
    request.getfuncargvalue.side_effect = lambda name: funcargs(name, request)
    request.tmpdir = tmpdir
    return request


def test_server_funcarg(request):
    server = pytest_couchdbkit.pytest_funcarg__couchdb_server(request)
    print server.info()

def test_database_dumping(request, tmpdir):
    db = pytest_couchdbkit.pytest_funcarg__couchdb(request)
    print db.info()
    db.save_doc({'_id': 'test'}, force_update=True)
    finalizer = request.addfinalizer.call_args[0][0]
    assert not tmpdir.join('couchdb.dump').check()
    finalizer()
    assert tmpdir.join('couchdb.dump').check()


def test_replication(request, tmpdir):
    server = pytest_couchdbkit.pytest_funcarg__couchdb_server(request)
    db_source = maybe_destroy_and_create(server, 'pytest_test_couchapp_source')
    db_source.save_doc({'_id': 'test'})


    db = pytest_couchdbkit.pytest_funcarg__couchdb(request)
    assert 'test' in db

