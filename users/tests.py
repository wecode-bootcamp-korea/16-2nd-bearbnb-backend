import jwt
import json
import boto3
import bcrypt

from django.test     import TestCase, Client
from unittest.mock   import patch, MagicMock

from .models         import User, SocialUser
from my_settings     import SECRET_KEY


client = Client()

@classmethod
class SignUpTest(TestCase):
    def setUpTestData(cls):
        User.objects.create(
            email      = 'yeonu@test.com',
            password   = 'testtest',
            name       = 'test test',
            country    = None,
            phone      = None,
            gender     = None,
            birthdate  = None,
        )
    
    def tearDown(self):
        User.objects.all().delete()

    @patch('boto3.client')
    def test_signup_post_success(self, mock_boto_client):
        client = boto3.client('s3') 
        user = json.dumps({
            'email'      : 'unittest@test.com',
            'password'   : 'testtest',
            'first_name' : 'test',
            'last_name'  : 'test',
            'country'    : None,
            'phone'      : None,
            'gender'     : None,
            'birthdate'  : None,
        })

        form = {
            'profile_photo': open('/home/yeonu//사진/Screenshot.png','rb'),
            'json':user
        }
        response = self.client.post('/users/signup', data=form)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message':'SUCCESS'})
    
    def test_signup_post_success_without_photo(self):
        user = json.dumps({
            'email'      : 'unittest@test.com',
            'password'   : 'testtest',
            'first_name' : 'test',
            'last_name'  : 'test',
            'country'    : None,
            'phone'      : None,
            'gender'     : None,
            'birthdate'  : None,
        })

        form = {
            'json':user
        }
        response = self.client.post('/users/signup', data=form)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message':'SUCCESS'})

    def test_signup_post_key_error(self): 
        user = json.dumps({
            '이메일'      : 'unittest@test.com',
            'password'   : 'testtest',
            'first_name' : 'test',
            'last_name'  : 'test',
            'country'    : None,
            'phone'      : None,
            'gender'     : None,
            'birthdate'  : None,

        })
        form = {
            'profile_photo': open('/home/yeonu//사진/p.jpeg','rb'),
            'json':user
        }
        response = self.client.post('/users/signup', data=form)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'KEY_ERROR'})

    def test_signup_post_email_duplicated(self):
        user = json.dumps({
            'email'      : 'yeonu@test.com',
            'password'   : 'testtest',
            'first_name' : 'test',
            'last_name'  : 'test',
            'country'    : None,
            'phone'      : None,
            'gender'     : None,
            'birthdate'  : None,
        })
        form = {
            'profile_photo': open('/home/yeonu//사진/p.jpeg','rb'),
            'json':user
        }
        response = self.client.post('/users/signup', data=form)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'USER_ALREADY_EXIST'})

    def test_signup_post_invalid_format_email(self): 
        user = json.dumps({
            'email'      : 'unittesttest.com',
            'password'   : 'testtest',
            'first_name' : 'test',
            'last_name'  : 'test',
            'country'    : None,
            'phone'      : None,
            'gender'     : None,
            'birthdate'  : None,

        })
        form = {
            'profile_photo': open('/home/yeonu//사진/p.jpeg','rb'),
            'json':user
        }
        response = self.client.post('/users/signup', data=form)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_FORMAT'})

    def test_signup_post_invalid_format_password(self): 
        user = json.dumps({
            'email'      : 'unittest@test.com',
            'password'   : 'test',
            'first_name' : 'test',
            'last_name'  : 'test',
            'country'    : None,
            'phone'      : None,
            'gender'     : None,
            'birthdate'  : None,

        })
        form = {
            'profile_photo': open('/home/yeonu//사진/p.jpeg','rb'),
            'json':user
        }
        response = self.client.post('/users/signup', data=form)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'INVALID_FORMAT'})


class SignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        password = 'testtest'.encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        User.objects.create(
           email      = 'test@test.com',
           password   = password,
           name       = 'test test',
           country    = None,
           phone      = None,
           gender     = None,
           birthdate  = None,
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signin_post_success(self):
        user = {
            'email'   :'test@test.com',
            'password':'testtest'
        }

        token    = jwt.encode({'id':User.objects.get(email='test@test.com').id}, SECRET_KEY, algorithm='HS256')
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'token':token})
    
    def test_signin_post_user_does_not_exist(self):
        user = {
            'email'   :'t@test.com',
            'password':'testtest'
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message':'USER_DOES_NOT_EXIST'})

    def test_signin_post_invalid_password(self):
        user = {
            'email'   :'test@test.com',
            'password':'wrongpassword'
        }
        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'INVALID_PASSWORD'})