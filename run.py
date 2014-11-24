from flask.ext.script import Manager
from app import application

manager = Manager(application)

@manager.command
def runserver():
	application.run(debug = True)

if __name__=="__main__":
	manager.run()