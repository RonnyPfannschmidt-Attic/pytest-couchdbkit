from io import BytesIO
import json
import re

from couchdbkit import View, ViewResults

def iter_docs(db):
    view = db.view('_all_docs',  include_docs='true')
    return view.all()

def items(db):
    viewres = db.view('_all_docs',  include_docs='true')
    rows = viewres.all()
    for row in rows:
        item = row['doc']
        yield item

        attachments = item.get('_attachments', [])
        for name in sorted(attachments):
            #XXX: unicode when not stream?!
            yield db.fetch_attachment(item, name,stream=True).read()

def readchunkdata(fp):
    size = fp.readline().rstrip()
    if not size:
        return None
    assert size.isdigit()
    data = fp.read(int(size))
    fp.read(2) # \r\n
    return data

def iter_dump(fp):
    return iter(lambda: readchunkdata(fp), None)

def load_dump(fp, db):
    items = iter_dump(fp)
    info = next(items)
    for doc in items:
        item = json.loads(doc)
        del item['_rev']
        attachments = item.get('_attachments', ())
        for name in sorted(attachments):
            data = next(items)
            attachments[name]['data'] = data
            del attachments[name]['stub']
        db.save_doc(item)



def writechunk(fp, data):
    if isinstance(data, dict):
        data = json.dumps(data, indent=2)
    fp.write('%s\r\n' % (len(data)))
    fp.write(data)
    fp.write('\r\n')


def dump_db(db, fp):
    writechunk(fp, db.info())
    for item in items(db):
        writechunk(fp, item)


