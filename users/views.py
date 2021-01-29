import re
import jwt
import json
import boto3
import bcrypt
import requests
import my_settings

from django.http     import JsonResponse
from django.views    import View

from .models         import User
from my_settings     import SECRET_KEY


class SignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.POST['json'])
            password        = data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
            name            = data['first_name'] + ' ' + data['last_name']
            email_validator = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")

            if len(password) < 8 or not email_validator.match(data['email']):
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
                password      = hashed_password,
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