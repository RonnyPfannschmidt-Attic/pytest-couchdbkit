import json

def pytest_addoption(parser):
    parser.addini('couchdbkit_backend', 'socketpool backend we should use', default='thread')
    parser.addini('couchdbkit_suffix', 'database name suffix')

def pytest_funcarg__couchdb_server(request):
    from couchdbkit import Server
    return Server(backend=request.config.getini('couchdbkit_backend'))

def pytest_funcarg__couchdb(request):
    from couchdbkit import ViewResults, View
    server = request.getfuncargvalue('couchdb_server')
    tmpdir = request.getfuncargvalue('tmpdir')
    dbname = 'pytest_' + request.config.getini('couchdbkit_suffix')
    db = server.get_or_create_db(dbname)
    db.flush()

    def finalize_db():
        view = View(db, '_all_docs')
        items = ViewResults(view, include_docs='true').all()
        with tmpdir.join('_couchdb.json-lines').open('w') as fp:
            for item in items:
                fp.write(json.dumps(item['doc'], sort_keys=1) + '\n')
    request.addfinalizer(finalize_db)
    return db
    
