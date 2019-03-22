from datetime import datetime
from app import database, loginManager
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import os, random


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return self.role is not None and (self.role.permissions and permissions) == permissions

    def is_administrator(self):
        return False


loginManager.anonymous_user = AnonymousUser


class Article(database.Model):
    __searchable__ = ["title", "body"]

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False, unique=True)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    body = database.Column(database.Text, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)
    company_id = database.Column(database.Integer, database.ForeignKey("company.id"), nullable=True)
    image_file = database.Column(database.String(50), unique=False, nullable=True, default="app/static/homepagePics/blackgirls.jpg")
    comments = database.relationship("Comment", backref="article", lazy=True)
    views = database.Column(database.Integer, default=0)

    @staticmethod
    def generate_fake(count=1):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        company_count = Company.query.count()
        for i in range(count):
            user = User.query.offset(randint(0, user_count - 1)).first()
            company = Company.query.offset(randint(0, company_count - 1)).first()
            article = Article(title=forgery_py.lorem_ipsum.words(randint(1, 5)),
                            body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                            author=user,
                            company=company)
            database.session.add(article)
        database.session.commit()

    def __repr__(self):
        return "Article('{}', '{}')".format(self.title, self.date_posted)


class Comment(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    body = database.Column(database.Text, nullable=False)
    article_id = database.Column(database.Integer, database.ForeignKey("article.id"), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "Comment('{}', '{}', {}')".format(self.id, self.article_id, self.date_posted)


class Company(database.Model, UserMixin):
    __searchable__ = ["name"]

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), unique=True, nullable=False)
    address = database.Column(database.String(100), unique=True, nullable=False)
    city = database.Column(database.String(50), unique=False, nullable=False)
    zip_code = database.Column(database.String(20), unique=False, nullable=False)
    state = database.Column(database.String(50), unique=False, nullable=True)
    country = database.Column(database.String(50), unique=False, nullable=False)
    phone_number = database.Column(database.String(10), unique=True, nullable=False)
    email = database.Column(database.String(80), unique=True, nullable=False)
    logo = database.Column(database.String(50), unique=False, nullable=False, default="default_" + str(random.randint(1, len(os.listdir("app/static/profilePics")) + 1)) + ".jpg")
    website = database.Column(database.String(100), unique=True, nullable=True)
    password = database.Column(database.String(20), nullable=False)
    role_id = database.Column(database.Integer, database.ForeignKey("role.id"))
    products = database.relationship("Product", backref="company", lazy=True)
    articles = database.relationship("Article", backref="company", lazy=True)

    def __init__(self, **kwargs):
        super(Company, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(name="Company").first()

    def can(self, permissions):
        return self.role is not None and (self.role.permissions and permissions) == permissions

    @staticmethod
    def generate_fake(count=1):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            company = Company(name=forgery_py.name.company_name(),
                        address=forgery_py.address.street_address(),
                        city=forgery_py.address.city(),
                        zip_code=forgery_py.address.zip_code(),
                        state=forgery_py.address.state(),
                        country=forgery_py.address.country(),
                        phone_number=''.join(["%s" % randint(0, 9) for num in range(0, 10)]),
                        email=forgery_py.email.address(),
                        password=forgery_py.basic.password())
            database.session.add(company)
        database.session.commit()

    def is_company(self):
        return self.can(Permission.MANAGE_PRODUCTS)

    def set_role(self, role):
        self.role = Role.query.filter_by(name=role).first()


@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))


class Permission:
    WRITE_ARTICLES = 2
    COMMENT = 4
    MODERATE_COMMENTS = 8
    MANAGE_PRODUCTS = 16
    ADMINISTER = 32


class Product(database.Model):
    __searchable__ = ["name", "price"]

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), unique=True, nullable=False)
    price = database.Column(database.String(10), nullable=False, default=0)
    description = database.Column(database.Text, nullable=False)
    image_file = database.Column(database.String(50), unique=False, nullable=False, default="default_" + str(random.randint(1, len(os.listdir("app/static/profilePics")) + 1)) + ".jpg")
    company_id = database.Column(database.Integer, database.ForeignKey("company.id"), nullable=True)
    reviews = database.relationship("Review", backref="product", lazy=True)

    @staticmethod
    def generate_fake(count=1):
        from random import seed
        import forgery_py

        seed()
        company_count = Company.query.count()
        for i in range(count):
            company = Company.query.offset(randint(0, company_count - 1)).first()
            product = Review(name=forgery_py.lorem_ipsum.words(randint(1, 3)),
                            price=forgery_py.monetary.money(),
                            description=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                            company=company)
            database.session.add(product)
        database.session.commit()

class Review(database.Model):
    __searchable__ = ["title", "body"]

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    body = database.Column(database.Text, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)
    product_id = database.Column(database.Integer, database.ForeignKey("product.id"), nullable=False)

    @staticmethod
    def generate_fake(count=1):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        product_count = Product.query.count()
        for i in range(count):
            user = User.query.offset(randint(0, user_count - 1)).first()
            product = Product.query.offset(randint(0, product_count - 1)).first()
            review = Review(title=forgery_py.lorem_ipsum.words(randint(1, 5)),
                            body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                            author=user,
                            product=product)
            database.session.add(review)
        database.session.commit()

    def __repr__(self):
        return "Review('{}', '{}')".format(self.title, self.date_posted)


class Role(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), unique=True)
    default = database.Column(database.Boolean, default=False, index=True)
    permissions = database.Column(database.Integer)
    users = database.relationship("User", backref="role", lazy="dynamic")
    companies = database.relationship("Company", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permissions += permission

    def has_permission(self, permission):
        return self.permissions and permission == permission

    @staticmethod
    def insert_roles():

        default_role = "User"
        roles = {
            "User": [Permission.COMMENT, Permission.WRITE_ARTICLES, Permission.MODERATE_COMMENTS],
            "Company": [Permission.MANAGE_PRODUCTS],
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

    def remove_permission(self, permission):
        if self.has_permission(permission):
            self.permissions -= permission

    def reset_permissions(self):
        self.permissions = 0


class User(database.Model, UserMixin):
    __searchable__ = ["firstname", "lastname", "username"]

    id = database.Column(database.Integer, primary_key=True)
    firstname = database.Column(database.String(32), unique=False, nullable=False)
    lastname = database.Column(database.String(32), unique=False, nullable=False)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(80), unique=True, nullable=False)
    image_file = database.Column(database.String(50), unique=False, nullable=False, default="default_" + str(random.randint(1, len(os.listdir("app/static/profilePics")) + 1)) + ".jpg")
    occupation = database.Column(database.String(50), unique=False, nullable=True)
    phone_number = database.Column(database.String(10), unique=True, nullable=True)
    bio = database.Column(database.Text, nullable=True)
    password = database.Column(database.String(100), nullable=False)
    role_id = database.Column(database.Integer, database.ForeignKey("role.id"))
    articles = database.relationship("Article", backref="author", lazy=True)
    comments = database.relationship("Comment", backref="commenter", lazy=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email in current_app.config["THECULTURE_ADMIN"]:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and (self.role.permissions and permissions) == permissions

    @staticmethod
    def generate_fake(count=1):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            user = User(firstname=forgery_py.name.first_name(),
                        lastname=forgery_py.name.last_name(),
                        username=forgery_py.internet.user_name(True),
                        email=forgery_py.email.address(),
                        password=forgery_py.basic.password())
            database.session.add(user)
        database.session.commit()

    def get_reset_token(self, expires_sec=180):
    	s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
    	return s.dumps({"user_id" : self.id})

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def set_role(self, role):
        self.role = Role.query.filter_by(name=role).first()

    @staticmethod
    def verify_reset_token(token):
    	s = Serializer(current_app.config["SECRET_KEY"])
    	try:
    		user_id = s.loads(token)["user_id"]
    	except:
    		return None
    	return User.query.get(user_id)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username, self.email, self.image_file)
