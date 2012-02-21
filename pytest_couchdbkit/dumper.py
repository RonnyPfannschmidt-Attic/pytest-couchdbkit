from io import BytesIO
import json


from couchdbkit import View, ViewResults

def iter_docs(db):
    view = db.view('_all_docs',  include_docs='true')
    return view.all()

def iter_attachments(db, item):
    return ()


def writechunk(fp, data):
    if isinstance(data, dict):
        data = json.dumps(data, indent=2)
    fp.write('%s\r\n' % (len(data)))
    fp.write(data)
    fp.write('\r\n')


def dump_db(db, dest):
    fp = open(dest, 'w')
    writechunk(fp, {
        'dest': dest,
        'db': db.info(),
    })


    

    for item in iter_docs(db):
        writechunk(fp, item)

        attachments = item.get('_attachments', [])
        for name in attachments:
            data = db.fetch_attachment(item, name)
            writechunk(fp, data)
    fp.close()
