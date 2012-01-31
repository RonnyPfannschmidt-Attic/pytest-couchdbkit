import pytest_couchdbkit
import couchdbkit
import mock
import json
settings = {'couchdbkit_suffix': 'test', 'couchdbkit_backend': 'thread'}


def funcargs(name, request):
    if name == 'couchdb_server':
        return couchdbkit.Server()
    print 'get funcarg', name
    return getattr(request, name)

def pytest_funcarg__request(request):
    request = mock.MagicMock()
    request.config.getini.side_effect = settings.get
    request.getfuncargvalue.side_effect = lambda name: funcargs(name, request)
    return request


def test_server_funcarg(request):
    server = pytest_couchdbkit.pytest_funcarg__couchdb_server(request)
    print server.info()

def test_database_dumping(request):
    db = pytest_couchdbkit.pytest_funcarg__couchdb(request)
    print db.info()
    db.save_doc({'_id': 'test'})
    finalizer = request.addfinalizer.call_args[0][0]
    finalizer()
    calls = request.tmpdir.join('_couchdb.json-lines').open('w').__enter__().write.call_args_list
    (args, kw) ,= calls
    assert not kw
    data = json.loads(args[0])
    print data
    del data['_rev']
    assert data == {'_id': 'test'}

