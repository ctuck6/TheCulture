from app import create_app, database
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import unittest, coverage, os

app = create_app()
app.app_context().push()

migrate = Migrate(app, database)
manager = Manager(app)
manager.add_command("database", MigrateCommand)

@manager.command
def test():
    tests = unittest.TestLoader().discover('test_app')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(
        branch=True,
        include='app/*'
    )
    cov.start()
    tests = unittest.TestLoader().discover('test_app')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print 'Coverage Summary:'
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()

if __name__ == '__main__':
	manager.run()