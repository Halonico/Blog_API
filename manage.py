import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.models.UserModel import UserModel
from src.models.BlogpostModel import BlogpostModel
from src.app import create_app, db

#Create the app to be able to do migration
app = create_app(os.getenv('FLASK_ENV'))
#Create the migration
#A migration is a file containing all the operations to make inside the database at a moment.
#It contains also the operations to undo thoses modifications inside the database
#It is like a commit in github, you can rollback step by step when you have problems. Its like a checkpoint in a videogame
migrate = Migrate(app=app, db=db, user=UserModel, blog=BlogpostModel)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()