from app import create_app, database
from flask import url_for
import unittest
from app.models import *


class FlaskClientTestCase(unittest.TestCase):

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

    def test_register_and_login(self):
        params = {
            "firstname": "john",
            "lastname": "smith",
            "username": "john1",
            "email": "john@example.com",
            "password": "password",
            "confirmPassword": "password"
        }
        response = self.client.post(url_for("users.register"), data=params)
        data = response.get_data(as_text=True)
        self.assertTrue("Your account has been created! Please sign in!" in data)
        self.assertTrue(response.status_code == 200)

        # login with the new account
        response = self.client.post(url_for("users.login"), data={
            "email": "john@example.com",
            "password": "password"
        }, follow_redirects=True)
        self.assertTrue(response.status_code == 200)

        # send a confirmation token
        user = User.query.filter_by(email="john@example.com").first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for("main.home", token=token), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue("Welcome!" in data)

        # log out
        response = self.client.get(url_for("users.logout"), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue("You have been logged out" in data)
