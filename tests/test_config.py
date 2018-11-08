from app.config import TestConfig
from app import create_app, database
import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session


@pytest.fixture(scope='session')
def app(request):
    app = create_app(TestConfig)
    app.app_context().push()

    # def teardown():
    #     app.app_context().pop()

    # request.addfinalizer(teardown)
    # return app
    with app.app_context():
        # alternative pattern to app.app_context().push()
        # all commands indented under 'with' are run in the app context
        database.create_all()
        yield app   # Note that we changed return for yield, see below for why
        database.session.remove()  # looks like db.session.close() would work as well
        database.drop_all()
        # return app


# @pytest.fixture(scope="session")
# def engine():
#     return create_engine("sqlite:///site.db")


# @pytest.yield_fixture(scope="session")
# def tables(app, engine):
#     database.app = app
#     database.create_all(engine)
#     yield
#     database.drop_all(engine)


# @pytest.yield_fixture
# def dbsession(engine, tables):
#     connection = engine.connect()
#     # begin the nested transaction
#     transaction = connection.begin()
#     # use the connection with the already started transaction
#     session = Session(bind=connection)

#     yield session

#     session.close()
#     # roll back the broader transaction
#     transaction.rollback()
#     # put back the connection to the connection pool
#     connection.close()


# @pytest.fixture(scope="session")
# def db(app, request):

#     def teardown():
#         database.drop_all()

#     database.app = app
#     database.create_all()

#     request.addfinalizer(teardown)
#     return database


# @pytest.fixture(scope="function")
# def session(db, request):
#     """Creates a new database session for a test."""
#     connection = db.engine.connect()
#     transaction = connection.begin()

#     options = dict(bind=connection, binds={})
#     session = db.create_scoped_session(options=options)

#     db.session = session

#     def teardown():
#         transaction.rollback()
#         connection.close()
#         session.remove()

#     request.addfinalizer(teardown)
#     return session
