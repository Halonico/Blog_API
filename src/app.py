from flask import Flask
from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint # add this line
from .views.BlogView import blogpost_api as blogpost_blueprint
def create_app(env_name):
  #Create a flask app
  app = Flask(__name__)
  #Set the behavior of the app from the environment name
  app.config.from_object(app_config[env_name])
  #Init the library to hash the password
  bcrypt.init_app(app)
  #Init the ORM
  #A ORM is used to make operation to the database without using sql request.
  #Like that, you can make directly make operations on the model in a pleasant syntax, and It will translate what you did in sql.
  db.init_app(app)
  #Just add a new route to the api
  #Every call on www.mywebsite.be/api/users will be transfered to the file UserView.py
  app.register_blueprint(user_blueprint,url_prefix='/api/users')
  app.register_blueprint(blogpost_blueprint,url_prefix='/api/blogs')
  return app
