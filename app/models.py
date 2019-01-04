from datetime import datetime
from app import database, loginManager
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from users.utils import savePicture
import os, random


class Permission:
    COMMENT = 2
    WRITE_ARTICLES = 4
    MODERATE_COMMENTS = 8
    ADMINISTER = 16


class Role(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), unique=True)
    default = database.Column(database.Boolean, default=False, index=True)
    permissions = database.Column(database.Integer)
    users = database.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        default_role = "User"

        roles = {
            "User": [Permission.COMMENT, Permission.WRITE_ARTICLES, Permission.MODERATE_COMMENTS],
            "Administrator": [Permission.COMMENT, Permission.WRITE_ARTICLES, Permission.MODERATE_COMMENTS, Permission.ADMINISTER]
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for permission in roles[r]:
                role.add_permission(permission)
            role.default = (role.name == default_role)
            database.session.add(role)
        database.session.commit()

    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permissions += permission

    def remove_permission(self, permission):
        if self.has_permission(permission):
            self.permissions -= permission

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, permission):
        return self.permissions and permission == permission


class User(database.Model, UserMixin):
    __searchable__ = ["firstname", "lastname", "username"]

    id = database.Column(database.Integer, primary_key=True)
    firstname = database.Column(database.String(32), unique=False, nullable=False)
    lastname = database.Column(database.String(32), unique=False, nullable=False)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(80), unique=True, nullable=False)
    image_file = database.Column(database.String(20), unique=False, nullable=False, default="default_" + str(random.randint(1, len(os.listdir("app/static/profilePics")) + 1)) + ".jpg")
    password = database.Column(database.String(80), nullable=False)
    role_id = database.Column(database.Integer, database.ForeignKey("role.id"))
    reviews = database.relationship("Review", backref="author", lazy=True)
    comments = database.relationship("Comment", backref="commenter", lazy=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email in current_app.config["THECULTURE_ADMIN"]:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def set_role(self, role):
        self.role = Role.query.filter_by(name=role).first()

    def can(self, permissions):
        return self.role is not None and (self.role.permissions and permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @staticmethod
    def generate_fake(count=1):
        from sqlalchemy import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            user = User(firstname=forgery_py.name.first_name(),
                        lastname=forgery_py.name.last_name(),
                        username=forgery_py.internet.user_name(True),
                        email=forgery_py.internet.email_address(),
                        password=forgery_py.lorem_ipsum.word())
            database.session.add(user)
            try:
                database.session.commit()
            except IntegrityError:
                database.session.rollback()

    def get_reset_token(self, expires_sec=180):
    	s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
    	return s.dumps({"userId" : self.id})

    @staticmethod
    def verify_reset_token(token):
    	s = Serializer(current_app.config["SECRET_KEY"])
    	try:
    		userId = s.loads(token)["userId"]
    	except:
    		return None
    	return User.query.get(userId)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username, self.email, self.image_file)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


loginManager.anonymous_user = AnonymousUser


@loginManager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))


class Review(database.Model):
    __searchable__ = ["title", "body"]

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    body = database.Column(database.Text, nullable=False)
    userId = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)
    comments = database.relationship("Comment", backref="review", lazy=True)
    views = database.Column(database.Integer, default=0)

    @staticmethod
    def generate_fake(count=1):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        for i in range(count):
            user = User.query.offset(randint(0, user_count - 1)).first()
            review = Review(title=forgery_py.lorem_ipsum.words(randint(1, 5)),
                            body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                            author=user)
            database.session.add(review)
            try:
                database.session.commit()
            except IntegrityError:
                database.session.rollback()

    def __repr__(self):
        return "Review('{}', '{}')".format(self.title, self.date_posted)


class Comment(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    body = database.Column(database.Text, nullable=False)
    reviewId = database.Column(database.Integer, database.ForeignKey("review.id"), nullable=False)
    userId = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "Comment('{}', '{}', {}')".format(self.id, self.reviewId, self.date_posted)
