# Generated by Django 3.1.5 on 2021-02-04 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
        migrations.CreateModel(
            name='SocialUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_user', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('profile_photo', models.URLField(max_length=2000, null=True)),
            ],
            options={
                'db_table': 'social_users',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, null=True)),
                ('name', models.CharField(max_length=45)),
                ('password', models.CharField(default='', max_length=1000)),
                ('gender', models.CharField(max_length=20, null=True)),
                ('birthdate', models.DateField(null=True)),
                ('email', models.EmailField(max_length=200)),
                ('profile_photo', models.URLField(max_length=2000, null=True)),
                ('is_email_valid', models.BooleanField(default=0)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.country')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.URLField(max_length=2000, null=True)),
                ('id_card_photo', models.URLField(max_length=2000, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'hosts',
            },
        ),
    ]
