import unittest
from app import database
from app.models import *

class TestQuery(unittest.TestCase):

    TEST_FIRSTNAME = "John"
    TEST_LASTNAME = "Doe"
    TEST_USERNAME = "Johnny1"
    TEST_EMAIL = "testuser@gmail.com"
    TEST_PASSWORD = "password"
    TEST_IMAGE_FILE = "default_1.jpg"


    def setUp(self):
        database.create_all(self.engine)
        sampleUser = User(TEST_FIRSTNAME, TEST_LASTNAME, TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD, TEST_IMAGE_FILE)
        database.session.add()
        sampleReview = Review("Sample Review", "This is a sample", "Johnny1")
        database.session.add()
        database.session.commit()

    def tearDown(self):
        database.drop_all(self.engine)

    def test_query_panel(self):
        expected = ["User('{}', '{}', '{}')".format(TEST_USERNAME, TEST_EMAIL, TEST_IMAGE_FILE)]
        result = Review.query.all()
        self.assertEqual(result, expected)