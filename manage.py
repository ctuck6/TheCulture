from app import create_app, database
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
app.app_context().push()

migrate = Migrate(app, database)
manager = Manager(app)
manager.add_command("database", MigrateCommand)

if __name__ == '__main__':
	manager.run()