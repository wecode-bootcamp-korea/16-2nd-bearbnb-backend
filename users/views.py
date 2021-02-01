import re
import jwt
import json
import boto3
import bcrypt
import requests
import my_settings

from django.http     import JsonResponse
from django.views    import View

from .models         import User, SocialUser
from my_settings     import SECRET_KEY


class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.POST['json'])
            name            = data['first_name'] + ' ' + data['last_name']
            email_validator = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")

            if len(data['password']) < 8 or not email_validator.match(data['email']):
                return JsonResponse({'message':'INVALID_FORMAT'}, status=400)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'USER_ALREADY_EXIST'}, status=400)

            s3_client = boto3.client(
            's3',
            aws_access_key_id=my_settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=my_settings.AWS_SECRET_ACCESS_KEY
            ) 

            if request.FILES.get('profile_photo'):
                file = request.FILES['profile_photo']
                s3_client.upload_fileobj(
                    file,
                    my_settings.BUCKET,
                    file.name,
                    ExtraArgs={
                        "ContentType":file.content_type
                    }
                )

                image_url_form = "https://s3.{bucket_location}.amazonaws.com/{bucket}/{profile_photo}"
               
                image_url = image_url_form.format(
                bucket_location = my_settings.BUCKET_LOCATION,
                bucket          = my_settings.BUCKET,
                profile_photo   = request.FILES['profile_photo']
                )
            else:
                image_url = None

            User(
                email         = data['email'],
                password      = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name          = name,
                profile_photo = image_url,
                country       = None,
                phone         = None,
                gender        = None,
                birthdate     = None
            ).save()

            return JsonResponse({'message':'SUCCESS'}, status=201)
            
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            password = data['password']

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=400)
            
            user           = User.objects.get(email=data['email'])
            password_check = user.password

            if bcrypt.checkpw(password.encode('utf-8'), password_check.encode('utf-8')):
                token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm='HS256')
                return JsonResponse({'token':token}, status=200)
            return JsonResponse({'message':'INVALID_PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class SocialLoginView(View):
    def post(self, request):
        try:
            social_access_token = request.headers['Authorization']
            url          = 'https://kapi.kakao.com/v2/user/me'
            headers      = {
                'Authorization' : f'Bearer {social_access_token}',
                'Content-type'  : 'application/x-www-form-urlencoded;charset=utf-8'
            }

            response        = requests.get(url, headers=headers)
            social_response = response.json()
            
            if social_response.get('code') == -401:
                return JsonResponse({'message':'INVALID_ACCESS_TOKEN'}, status=401)
            
            if not SocialUser.objects.filter(social_user=social_response['id']).exists():
                SocialUser(
                    social_user   = social_response['id'],
                    email         = social_response['kakao_account']['email'],
                    profile_photo = social_response['properties']['profile_image']
                ).save()

            access_token = jwt.encode({'id':SocialUser.objects.get(social_user=social_response['id']).id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'access_token':access_token},status=200)

        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)