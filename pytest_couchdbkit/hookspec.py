

def pytest_couchdbkit_push_app(database):
    """
    invoked to push couchapps to a replication source database
    that is replicated to the target for each test
    """
