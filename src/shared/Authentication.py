import jwt
import os
import datetime
from flask import json, Response, request, g
from ..models.UserModel import UserModel
from functools import wraps
#This class is used to authentificate a user, it will manage the JWT token
#See the UserView for more explanation
class Auth():
  """
  Auth Class
  """
  #This will generate a token, and we are going to put the user id in it
  @staticmethod
  def generate_token(user_id):
    """
    Generate Token Method
    """
    try:
      payload = {
        #Expiration date, like that if the token is stolen, it will be usefull only during 1 day
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        #Creation date
        'iat': datetime.datetime.utcnow(),
        #User id, to know which user it is 
        'sub': user_id
      }
      #This method will encode the jwt token, like that, if it's modified, the signature will be incorrect and the jwt will be not usable
      return jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY'),
        #"ISSOULABOUGNADAIRE",
        'HS256'
      ).decode("utf-8")
    except Exception as e:
      return Response(
        mimetype="application/json",
        response=json.dumps({'error': 'error in generating user token'}),
        status=400
      )
  #Check if the token is still correct
  #This decorator says that we don't need to create a Authentication object to use this function
  @staticmethod
  def decode_token(token):
    """
    Decode token method
    """
    re = {'data': {}, 'error': {}}
    try:
      payload = jwt.decode(token,os.getenv('JWT_SECRET_KEY'))
      re['data'] = {'user_id': payload['sub']}
      return re
    except jwt.ExpiredSignatureError as e1:
      re['error'] = {'message': 'token expired, please login again'}
      return re
    except jwt.InvalidTokenError:
      re['error'] = {'message': 'Invalid token, please try again with a new token'}
      return re
  #Check if the token is correct and the user exist
  @staticmethod
  def auth_required(func):
    """
    Auth decorator
    """
    @wraps(func)
    def decorated_auth(*args, **kwargs):
      #Check if the token is in the header of the token
      if 'api-token' not in request.headers:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
          status=400
        )
      #Decode the token
      token = request.headers.get('api-token')
      data = Auth.decode_token(token)
      if data['error']:
        return Response(
          mimetype="application/json",
          response=json.dumps(data['error']),
          status=400
        )
      #Check if the user is preset in the database by the id
      user_id = data['data']['user_id']
      check_user = UserModel.get_one_user(user_id)
      if not check_user:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'user does not exist, invalid token'}),
          status=400
        )
      g.user = {'id': user_id}
      return func(*args, **kwargs)
    return decorated_auth
