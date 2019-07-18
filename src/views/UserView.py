from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema,UserSchemaCreate
from ..shared.Authentication import Auth

#Set the name of the blueprint
user_api = Blueprint('users', __name__)
#The user_schema is used like a template to send the information of the database to the user of the api
#Like that, we can, for example, send a user without the password field.
user_schema_create = UserSchemaCreate()
user_schema = UserSchema()
#This define a route for the api, every POST request on /users will be send here.
#A POST request is used when you want to create something in the API, or send data to be processed
#So we are on the route /users/, doing a post, we are going to create a user
@user_api.route('/', methods=['POST'])
def create():
  """
  Create User Function
  """
  #Retreive the data sended by the user, and read it as json
  #Json is a way to send data between two entities, you can compare it to a dictionnary in pythons
  req_data = request.get_json()
  #So every field in the json will be match in the user_schema, and create a python dictionnary called data
  data, error = user_schema_create.load(req_data)
  #If there is a error during the load, send a 400 error
  #For example, in the schema, we sayed that the password was required, and there is no password in the sended data. That will create a error
  if error:
    return custom_response(error, 400)
  # check if user already exist in the db by it's email
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  if user_in_db:
    message = {'error': 'User already exist, please supply another email address'}
    return custom_response(message, 400)
  #Create a user object from the data
  user = UserModel(data)
  #Save it inside the database
  user.save()

  ser_data = user_schema.dump(user).data
  #This will create a token with the id of the user in it.
  #A token is like a bracelet in a nightclub.
  #It's says who you are (id), it contains the date when it was created and when it expire,
  #so you can go outside smoke a cigarette and enter again with no problem.
  #But tomorrow, it will be expired, and you can't enter anymore.
  #You can put everything you want in a jwt, but be carefull, it can be read by anyone but can't be modified.
  #For example, in a nightclub, you can have a special mark to be vip. In a jwt, you can add any attribute (ex : a role (admin,user),etc...)
  #It is put in the header of the request, and will be inside the header in every request to know which user made the call
  token = Auth.generate_token(ser_data.get('id'))
  return custom_response({'jwt_token': token}, 201)
#Every get request on /users are processed here
#A GET request is made when you want to access ressources, for example here, the list of users
@user_api.route('/', methods=['GET'])
#Call the method auth_required in Authentification.py
#It will read the header, get the jwt and check if it wasn't altered
#If it's not, it will run the get_all()
@Auth.auth_required
def get_all():
  #Get all user
  users = UserModel.get_all_users()
  #Transform it before sending it (like that, the user won't have the hashed password)
  ser_users = user_schema.dump(users, many=True).data
  return custom_response(ser_users, 200) 
#Same as before
@user_api.route('/login', methods=['POST'])
def login():
  #Get the json data
  req_data = request.get_json()
  #Parse it to python's dict
  data, error = user_schema_create.load(req_data, partial=True)

  if error:
    return custom_response(error, 400)
  #If the dictionnary doesn't contain the email and password key, it will send a error to the client
  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  #Else, it will search for a user with the corresponding email
  user = UserModel.get_user_by_email(data.get('email'))
  #If there is no user in the database with the email, send error
  if not user:
    return custom_response({'error': 'invalid credentials'}, 400)
  #If the 2 password are differents, return a error
  if not user.check_hash(data.get('password')):
    return custom_response({'error': 'invalid credentials'}, 400)
  #Parse user
  ser_data = user_schema_create.dump(user).data
  #Create a token
  token = Auth.generate_token(ser_data.get('id'))
  #Send token
  return custom_response({'jwt_token': token}, 200)
#Every get request on /users/a_number will be processed here
#Here it's a get request to get only one specific user by it's id
#YOU NEED TO PUT IT AFTER THE GET ALL ROUTE
#Elsewhere, every request will be processed by the get id one, and it will think there is a missing number
@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
  """
  Get a single user
  """
  user = UserModel.get_one_user(user_id)
  if not user:
    return custom_response({'error': 'user not found'}, 404)
  
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)
#A put request is often used to update a entity / row in database
@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
  """
  Update me
  """
  req_data = request.get_json()
  data, error = user_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)

  user = UserModel.get_one_user(g.user.get('id'))
  user.update(data)
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)
#Delete it's own account in the app
@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
  """
  Delete a user
  """
  user = UserModel.get_one_user(g.user.get('id'))
  user.delete()
  return custom_response({'message': 'deleted'}, 204)
#Get it's own account in the app
@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  """
  Get me
  """
  user = UserModel.get_one_user(g.user.get('id'))
  ser_user = user_schema.dump(user).data
  return custom_response(ser_user, 200)
def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )