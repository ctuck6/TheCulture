from app import create_app, database
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import unittest, coverage, os, sys
from app.models import *

# heroku run python manage.py deploy
# heroku restart

app = create_app()
app.app_context().push()

COV = None
if os.environ.get("FLASK_COVERAGE"):
    COV = coverage.coverage(branch=True, include="app/*")
    COV.start()

migrate = Migrate(app, database)
manager = Manager(app)


def make_shell_context():
    return dict(app=app,
                database=database,
                User=User, Review=Review,
                Comment=Comment,
                Role=Role,
                Company=Company,
                Product=Product)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("database", MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get("FLASK_COVERAGE"):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        print("HTML version: file://%s/index.html" % covdir)
        COV.erase()


if __name__ == "__main__":
	manager.run()
