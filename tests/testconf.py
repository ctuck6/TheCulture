from app.config import TestConfig
from app import create_app, database
import pytest


@pytest.fixture(scope='session')
def app(request):
    app = create_app(TestConfig)
    app.app_context().push()

    def teardown():
        app.app_context().pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):

    def teardown():
        database.drop_all()

    database.app = app
    database.create_all()

    request.addfinalizer(teardown)
    return database


@pytest.fixture(scope="function")
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
