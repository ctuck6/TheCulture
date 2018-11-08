import unittest
from flask import current_app, url_for
from app import create_app, database
from flask_login import current_user
from flask_api import status


class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        database.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        database.session.remove()
        database.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for("main.home"))
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(current_user.is_authenticated)

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])
