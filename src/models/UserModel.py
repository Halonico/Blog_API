from marshmallow import fields, Schema
import datetime
from . import db
from ..app import bcrypt
from .BlogpostModel import BlogpostSchema
#This class is used to make request to the database
#It's a representation of the table in the database
class UserModel(db.Model):
  """
  User Model
  """

  # table name
  __tablename__ = 'users'
  #Define each field of the table users
  #A primary key is unique and indexed, it is used to identify a specific row in the database, and is used to make relations and joins
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  #Set the relation with de BlogpostModel
  blogposts = db.relationship('BlogpostModel', backref='users', lazy=True) # add this new line

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.email = data.get('email')
    #Hash the password when we create the model
    self.password = self.__generate_hash(data.get('password'))
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()
  #Create the model in the database
  def save(self):
    db.session.add(self)
    db.session.commit()
  #Update the user in the database
  def update(self, data):
    #Check if there is a new password, and hash it if it's the case
    for key, item in data.items():
      if key == 'password': # add this new line
        self.password = self.__generate_hash(item) # add this new line
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()
  #Delete the model in the database, it will use the id of the model
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  #Check if the password of the model is correct
  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)
  #Retreive every users
  @staticmethod
  def get_all_users():
    return UserModel.query.all()
  #Retreive only one user by it's id 
  @staticmethod
  def get_one_user(id):
    return UserModel.query.get(id)
  #Retreive only one user by it's email
  @staticmethod
  def get_user_by_email(emailTmp):
    return db.session.query(UserModel).filter_by(email=emailTmp).first() 
  #Used to print the user in case of ...
  def __repr(self):
    return '<id {}>'.format(self.id)
#Template when we need to create a user
class UserSchemaCreate(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  #Says there is a array of Blog
  blogposts = fields.Nested(BlogpostSchema, many=True)
#Template for everything else
class UserSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  email = fields.Email(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  #Says there is a array of Blog
  blogposts = fields.Nested(BlogpostSchema, many=True)