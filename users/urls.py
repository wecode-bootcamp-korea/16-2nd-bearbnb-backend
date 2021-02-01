from django.urls import path
from .views      import SignUpView, SignInView, SocialLoginView


urlpatterns = [
   path('/signup', SignUpView.as_view()),
   path('/signin', SignInView.as_view()),
   path('/social', SocialLoginView.as_view()),
]
