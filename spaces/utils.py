import jwt

from django.http     import JsonResponse

import my_settings
from users.models    import User, Host

def login_required(function):

    def wrapper(self, request, *args):
        try:
            access_token = request.headers.get("Authorization")
            if not access_token:
                return JsonResponse({'message': 'LOGIN_REQUIRED'}, status=401)
            
            header = jwt.decode(access_token, my_settings.SECRET_KEY, algorithms=my_settings.ALGORITHM)
            if not User.objects.filter(id = header['id']).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            
            setattr(request, "user", User.objects.get(id = header['id']))
            return function(self, request, *args)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'JWT_DECODE_ERROR'}, status=400)

    return wrapper

def host_required(function):

    def wrapper(self, request, *args):
        try:
            user  = request.user
            hosts = Host.objects.filter(user=user)
            if not hosts.exists():
                return JsonResponse({'message': 'INVALID_HOST'}, status=401)

            host  = hosts.get() 
            setattr(request, "host", host)
            return function(self, request, *args)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'JWT_DECODE_ERROR'}, status=400)

    return wrapper


