from app import create_app
from flask_whooshalchemyplus import index_all

app = create_app()
app.app_context().push()
index_all(app)

if __name__ == "__main__":
	app.run(debug = True)
