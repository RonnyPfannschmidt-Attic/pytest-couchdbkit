
from pytest_couchdbkit.dumper import items, dump_db, load_dump
from io import BytesIO

def test_items_simple(couchdb):
    
    empty = list(items(couchdb))
    assert empty == []

    doc = {'_id': 'test'}
    couchdb.save_doc(doc)

    first = list(items(couchdb))
    assert len(first) == 1
    assert first[0] == doc


    couchdb.put_attachment(doc, 'data', name='foo.py')

    first_attach = list(items(couchdb))
    adoc, data = first_attach
    assert adoc == doc
    assert data == 'data'


def test_ddoc(couchdb):
    ddoc = {'_id': '_design/test'}
    couchdb.save_doc(ddoc)
    ddocs = list(items(couchdb))
    assert ddocs == [ddoc]

def test_dump_load(couchdb_server):
    db = couchdb_server.get_or_create_db('test_dumping_db')
    db.flush()
    assert db.info()['doc_count'] == 0
    doc = {'_id': 'test'}
    db.save_doc(doc)
    assert db.info()['doc_count'] == 1
    db.put_attachment(doc, 'test a', name='a.py')
    db.put_attachment(doc, 'test b', name='b.py')
    io = BytesIO()
    dump_db(db, io)
    db.flush()
    assert db.info()['doc_count'] == 0
    io.seek(0)
    load_dump(io, db)

    assert db.info()['doc_count'] == 1
    assert db.fetch_attachment('test', 'a.py') == 'test a'
    assert db.fetch_attachment('test', 'b.py') == 'test b'
