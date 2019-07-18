import os
#Thoses class are used to change the behavior of the app when it's used in production or in development
#You can for example change the uri of the database, to use a different one in production or in development
#Like that, if you make a drop * by mistake, it will not affect the user on the app in the production
class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    #JWT_SECRET_KEY = "ISSOULABOUGNADAIRE"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    #SQLALCHEMY_DATABASE_URI = "postgres://postgres:halo7810@localhost:5432/mein_blog_api"
class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

app_config = {
    'development': Development,
    'production': Production,
}