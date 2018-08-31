from datetime import datetime
from app import db, loginManager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import random

@loginManager.user_loader
def loadUser(userId):
	return User.query.get(int(userId))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    image_file = db.Column(db.String(20), unique = False, nullable = False, default = "default_" + str(random.randint(1, 5)) + ".jpg")
    password = db.Column(db.String(20), nullable = False)
    reviews = db.relationship("Review", backref = "author", lazy = True)

    def get_reset_token(self, expires_sec = 300):
    	s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
    	s.dumps({"userId": self.id})

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

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    body = db.Column(db.Text, nullable = False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return "Review('{}', '{}')".format(self.title, self.date_posted)