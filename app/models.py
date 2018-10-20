import random
from datetime import datetime
from app import database, loginManager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from users.utils import savePicture
import flask_whooshalchemyplus
import os

@loginManager.user_loader
def loadUser(userId):
	return User.query.get(int(userId))

class User(database.Model, UserMixin):
    __searchable__ = ["firstname", "lastname", "username"]

    id = database.Column(database.Integer, primary_key = True)
    firstname = database.Column(database.String(32), unique = False, nullable = False)
    lastname = database.Column(database.String(32), unique = False, nullable = False)
    username = database.Column(database.String(20), unique = True, nullable = False)
    email = database.Column(database.String(80), unique = True, nullable = False)
    image_file = database.Column(database.String(20), unique = False, nullable = False, default = "default_" + str(random.randint(1, len(os.listdir("app/static/profilePics")) + 1)) + ".jpg")
    password = database.Column(database.String(80), nullable = False)
    reviews = database.relationship("Review", backref = "author", lazy = True)

    def get_reset_token(self, expires_sec = 180):
    	s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
    	return s.dumps({"userId" : self.id})

    @staticmethod
    def verify_reset_token(token):
    	s = Serializer(current_app.config["SECRET_KEY"])
    	try:
    		userId = s.loads(token)['userId']
    	except:
    		return None
    	return User.query.get(userId)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username, self.email, self.image_file)

class Review(database.Model):
    __searchable__ = ["title", "body"]

    id = database.Column(database.Integer, primary_key = True)
    title = database.Column(database.String(100), nullable = False)
    date_posted = database.Column(database.DateTime, nullable = False, default = datetime.utcnow)
    body = database.Column(database.Text, nullable = False)
    userId = database.Column(database.Integer, database.ForeignKey("user.id"), nullable = False)
    comments = database.relationship("Comment", backref = "review", lazy = True)

    def __repr__(self):
        return "Review('{}', '{}')".format(self.title, self.date_posted)

class Comment(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    date_posted = database.Column(database.DateTime, nullable = False, default = datetime.utcnow)
    body = database.Column(database.Text, nullable = False)
    reviewId = database.Column(database.Integer, database.ForeignKey("review.id"), nullable = False)
    commenter = database.Column(database.String(20), unique = False, nullable = False)

    def __repr__(self):
        return "Comment('{}', '{}', {}')".format(self.id, self.reviewId, self.date_posted)

