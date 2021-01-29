import jwt
import json
import bcrypt
import boto3

from django.test     import TestCase, Client
from unittest.mock   import patch

from .models         import User


client = Client()

class SignUpTest(TestCase):
    def setUp(self):
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