# Generated by Django 3.1.4 on 2021-01-29 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bedroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=25)),
            ],
            options={
                'db_table': 'bedrooms',
            },
        ),
        migrations.CreateModel(
            name='BedType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'bed_types',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('icon_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'options',
            },
        ),
        migrations.CreateModel(
            name='PlaceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'place_types',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'properties',
            },
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=18)),
                ('description', models.CharField(max_length=3000)),
                ('max_people', models.IntegerField(default=0)),
                ('bathroom', models.IntegerField(default=0)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('pub_date', models.DateField(auto_now_add=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.host')),
                ('place_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.placetype')),
            ],
            options={
                'db_table': 'spaces',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='SubProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('space_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.property')),
            ],
            options={
                'db_table': 'sub_properties',
            },
        ),
        migrations.CreateModel(
            name='SpaceTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.space')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.tag')),
            ],
            options={
                'db_table': 'space_tags',
            },
        ),
        migrations.CreateModel(
            name='SpaceOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.option')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.space')),
            ],
            options={
                'db_table': 'space_options',
            },
        ),
        migrations.AddField(
            model_name='space',
            name='sub_property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.subproperty'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateField(auto_now=True)),
                ('content', models.CharField(max_length=1000)),
                ('cleanliness_score', models.IntegerField(default=0)),
                ('communication_score', models.IntegerField(default=0)),
                ('check_in_score', models.IntegerField(default=0)),
                ('accuracy_score', models.IntegerField(default=0)),
                ('location_score', models.IntegerField(default=0)),
                ('value_score', models.IntegerField(default=0)),
                ('image_url', models.URLField(max_length=2000)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.space')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_with_host', models.BooleanField(default=0)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('adult', models.IntegerField()),
                ('children', models.IntegerField(null=True)),
                ('infant', models.IntegerField(null=True)),
                ('reservation_code', models.CharField(max_length=45)),
                ('cancellation_flexibility', models.BooleanField(default=0)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.space')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'reservations',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=45)),
                ('city', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=150)),
                ('address_detail', models.CharField(max_length=45)),
                ('letitude', models.DecimalField(decimal_places=6, max_digits=10, null=True)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.country')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.space')),
            ],
            options={
                'db_table': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2000)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.space')),
            ],
            options={
                'db_table': 'images',
            },
        ),
        migrations.CreateModel(
            name='BedroomBed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('bed_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.bedtype')),
                ('bedroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.bedroom')),
            ],
            options={
                'db_table': 'bedroom_beds',
            },
        ),
        migrations.AddField(
            model_name='bedroom',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaces.space'),
        ),
    ]
