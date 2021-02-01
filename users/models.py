from django.db import models


class User(models.Model):
    country        = models.ForeignKey('users.Country', on_delete = models.SET_NULL, null=True)
    phone          = models.CharField(max_length=20, null=True)
    name           = models.CharField(max_length=45)
    password       = models.CharField(max_length=1000, default='')
    gender         = models.CharField(max_length=20, null=True)
    birthdate      = models.DateField(null=True)
    email          = models.EmailField(max_length=200)
    profile_photo  = models.URLField(max_length=2000, null=True)
    is_email_valid = models.BooleanField(default=0)
    
    class Meta:
        db_table = 'users'


class SocialUser(models.Model):
    social_user   = models.CharField(max_length=45)
    email         = models.EmailField(max_length=100, null=True)
    profile_photo = models.URLField(max_length=2000, null=True)

    class Meta:
        db_table = 'social_users'


class Host(models.Model):
    user          = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile_photo = models.URLField(max_length=2000, null=True)
    id_card_photo = models.URLField(max_length=2000, null=True)

    class Meta:
        db_table = 'hosts'


class Country(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'countries'
