class Config():
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = "361f657555c5599857b926161b13403a"
	MAIL_SERVER = "smtp.googlemail.com"
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = "cameronrtucker21@gmail.com"
	MAIL_PASSWORD = "Waffles*11"