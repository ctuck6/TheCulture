from datetime import datetime
from app import database, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, g
import os, random


class AnonymousUser(AnonymousUserMixin):
    def __init__(self, **kwargs):
        super(AnonymousUser, self).__init__(**kwargs)
        self.role = Role.query.filter_by(name="User").first()

    def can(self, permissions):
        return self.role is not None and (self.role.permissions and permissions) == permissions

    @property
    def is_company(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Article(database.Model):
    __searchable__ = ["title", "body"]

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False, unique=True)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    body = database.Column(database.Text, nullable=False)
    user_id = database.Column(database.Unicode(36), database.ForeignKey("user.id"), nullable=False)
    company_id = database.Column(database.Unicode(36), database.ForeignKey("company.id"), nullable=True)
    image_file = database.Column(database.String(150), unique=False, nullable=True, default="app/static/homepagePics/blackgirls.jpg")
    comments = database.relationship("Comment", cascade="all,delete", backref="article", lazy="dynamic")
    views = database.Column(database.Integer, default=0)

    @staticmethod
    def generate_fake():
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        company_count = Company.query.count()
        for i in range(user_count):
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
    user_id = database.Column(database.Unicode(36), database.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "Comment('{}', '{}', {}')".format(self.id, self.article_id, self.date_posted)


class Company(database.Model, UserMixin):
    __searchable__ = ["name"]

    id = database.Column(database.Unicode(36), primary_key=True, autoincrement=False)
    name = database.Column(database.String(50), unique=True, nullable=False)
    address = database.Column(database.String(100), unique=True, nullable=False)
    city = database.Column(database.String(50), unique=False, nullable=False)
    zip_code = database.Column(database.String(20), unique=False, nullable=False)
    state = database.Column(database.String(25), unique=False, nullable=True)
    country = database.Column(database.String(50), unique=False, nullable=False)
    phone_number = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(80), unique=True, nullable=False)
    image_file = database.Column(database.String(150), unique=False, nullable=True,
        default="/static/profilePics/default_" + str(random.randint(1, len(os.listdir("app/static/profilePics")) + 1)) + ".jpg")
    website = database.Column(database.String(100), unique=True, nullable=True)
    password = database.Column(database.String(100), nullable=False)
    role_id = database.Column(database.Integer, database.ForeignKey("role.id"))
    products = database.relationship("Product", cascade="all,delete", backref="company", lazy="dynamic")
    articles = database.relationship("Article", cascade="all,delete", backref="company", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Company, self).__init__(**kwargs)
        self.role = Role.query.filter_by(name="Company").first()

    def can(self, permissions):
        return self.role is not None and (self.role.permissions and permissions) == permissions

    @staticmethod
    def generate_fake():
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(3):
            company = Company(name=forgery_py.name.company_name(),
                            address=forgery_py.address.street_address(),
                            city=forgery_py.address.city(),
                            zip_code=forgery_py.address.zip_code(),
                            state=forgery_py.address.state(),
                            country=forgery_py.address.country(),
                            phone_number=''.join(["%s" % randint(0, 9) for num in range(0, 10)]),
                            email=forgery_py.email.address(),
                            website=forgery_py.forgery.internet.domain_name(),
                            password=forgery_py.basic.password())
            database.session.add(company)
        database.session.commit()

    @property
    def is_company(self):
        return True

    def set_role(self, role):
        self.role = Role.query.filter_by(name=role).first()


items = database.Table("items",
    database.Column("user_id", database.Unicode(36), database.ForeignKey("user.id")),
    database.Column("product_id", database.Integer, database.ForeignKey("product.id"))
)


class Permission:
    WRITE_ARTICLES = 2
    COMMENT = 4
    MODERATE_COMMENTS = 8
    MANAGE_PRODUCTS = 16


class Product(database.Model):
    __searchable__ = ["name", "price"]

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), unique=True, nullable=False)
    price = database.Column(database.Integer, nullable=False, default=0.00)
    rating = database.Column(database.Integer, nullable=True, default=5)
    description = database.Column(database.Text, nullable=False)
    image_file = database.Column(database.String(150), unique=False, nullable=True,
        default="/static/profilePics/default_" + str(random.randint(1, len(os.listdir("app/static/profilePics")) + 1)) + ".jpg")
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    company_id = database.Column(database.Unicode(36), database.ForeignKey("company.id"), nullable=True)
    reviews = database.relationship("Review", cascade="all,delete", backref="product", lazy="dynamic")
    wishlist = database.relationship("User", secondary=items, backref=database.backref("wishlist", lazy="dynamic"))

    @staticmethod
    def generate_fake():
        from random import seed
        import forgery_py

        seed()
        company_count = Company.query.count()
        for i in range(company_count):
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
    rating = database.Column(database.Integer, nullable=False)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    body = database.Column(database.Text, nullable=False)
    user_id = database.Column(database.Unicode(36), database.ForeignKey("user.id"), nullable=False)
    product_id = database.Column(database.Integer, database.ForeignKey("product.id"), nullable=False)

    @staticmethod
    def generate_fake():
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        product_count = Product.query.count()
        for i in range(product_count):
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
            "Company": [Permission.COMMENT, Permission.WRITE_ARTICLES, Permission.MANAGE_PRODUCTS]
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


class MailingList(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email =  database.Column(database.String(80), unique=True, nullable=False)


class User(database.Model, UserMixin):
    __searchable__ = ["firstname", "lastname", "username"]

    id = database.Column(database.Unicode(36), primary_key=True, autoincrement=False)
    firstname = database.Column(database.String(32), unique=False, nullable=False)
    lastname = database.Column(database.String(32), unique=False, nullable=False)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(80), unique=True, nullable=False)
    image_file = database.Column(database.String(150), unique=False, nullable=True,
        default="/static/profilePics/default_" + str(random.randint(1, len(os.listdir("app/static/profilePics")) + 1)) + ".jpg")
    occupation = database.Column(database.String(50), unique=False, nullable=True)
    phone_number = database.Column(database.String(10), unique=True, nullable=True)
    hometown = database.Column(database.String(50), unique=False, nullable=True)
    bio = database.Column(database.Text, nullable=True)
    password = database.Column(database.String(100), nullable=False)
    role_id = database.Column(database.Integer, database.ForeignKey("role.id"))
    articles = database.relationship("Article", cascade="all,delete", backref="author", lazy="dynamic")
    comments = database.relationship("Comment", cascade="all,delete", backref="commenter", lazy="dynamic")
    reviews = database.relationship("Review", cascade="all,delete", backref="reviewer", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.role = Role.query.filter_by(name="User").first()

    def can(self, permissions):
        return self.role is not None and (self.role.permissions and permissions) == permissions

    @staticmethod
    def generate_fake():
        from random import seed
        import forgery_py

        seed()
        for i in range(3):
            user = User(firstname=forgery_py.name.first_name(),
                        lastname=forgery_py.name.last_name(),
                        username=forgery_py.internet.user_name(True),
                        email=forgery_py.email.address(),
                        password=forgery_py.basic.password())
            database.session.add(user)
        database.session.commit()

    def get_reset_token(self, expires_sec=300):
    	s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
    	return s.dumps({"user_id" : self.id})

    @property
    def is_company(self):
        return False

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
