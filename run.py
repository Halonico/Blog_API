import os
from src.app import create_app
if __name__ == '__main__':
  #This line retreive the environment name inside system's variables.
  #It allows the server to change his behavior by changing the value of env_name, by reaching the corresponding object in config.py
  #Like that, we can specify for exemple, one database specific for the development team for test purpose. And one for the production.
  #We can also enable the debbuger while we are in development mode
  env_name = os.getenv('FLASK_ENV')
  app = create_app(env_name)
  # run app
  app.run()