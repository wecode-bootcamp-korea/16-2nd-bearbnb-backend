import jwt
import my_settings

from django.http  import JsonResponse

from users.models import User

def login_required(function):
    def wrapper(self, request, *args):
        try:
            access_token = request.headers.get("Authorization")
            if not access_token:
                return JsonResponse({'MESSAGE': 'LOGIN_REQUIRED'}, status=401)
            header = jwt.decode(
                access_token,
                my_settings.SECRET_KEY,
                algorithms = 'HS256'
            )
            if not User.objects.filter(id = header['id']).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
            setattr(request, "user", User.objects.get(id = header['id']))
            return function(self, request, *args)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'JWT_DECODE_ERROR'}, status=400)
    return wrapper