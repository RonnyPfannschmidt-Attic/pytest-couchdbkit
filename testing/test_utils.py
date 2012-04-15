

from mock import Mock
from pytest_couchdbkit.utils import *

def config(**data):
    mock = Mock()
    mock.getini = data.get
    return mock


def test_dbname_from_config():
    conf = config(couchdbkit_suffix='fun')

    name = dbname_from_config(conf, '%s')
    assert name == 'fun'
