from app import create_app
from flask_whooshalchemyplus import index_all

app = create_app("development")
app.app_context().push()

if __name__ == "__main__":
	index_all(app)
	app.run(debug = True)
