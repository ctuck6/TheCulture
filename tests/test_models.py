import unittest
from flask import current_app, url_for
from app import create_app, database
from flask_login import current_user


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("test")
        self.app_context = self.app.app_context()
        self.app_context.push()
        database.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        database.session.remove()
        database.drop_all()
        self.app_context.pop()
