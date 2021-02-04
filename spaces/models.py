from django.db    import models
from users.models import Host


class Space(models.Model):
    host         = models.ForeignKey('users.Host', on_delete=models.CASCADE)
    name         = models.CharField(max_length=100, null=True)
    price        = models.DecimalField(max_digits=18 ,decimal_places=2, null=True)
    description  = models.CharField(max_length=3000, null=True)
    place_type   = models.ForeignKey('spaces.PlaceType', on_delete=models.CASCADE)
    sub_property = models.ForeignKey('spaces.SubProperty', on_delete=models.CASCADE)
    max_people   = models.IntegerField(default=0)
    bathroom     = models.IntegerField(default=0)
    rating       = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    pub_date     = models.DateField(auto_now_add=True)
    is_with_host = models.BooleanField(default=0, null=True)
    cleaning_fee = models.DecimalField(max_digits=18 ,decimal_places=2, null=True)
    
    class Meta:
        db_table = 'spaces'


class PlaceType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'place_types'


class Property(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'properties'


class SubProperty(models.Model):
    space_property = models.ForeignKey('spaces.Property', on_delete=models.CASCADE)
    name           = models.CharField(max_length=45)

    class Meta:
        db_table = 'sub_properties'


class Option(models.Model):
    name     = models.CharField(max_length=45)
    icon_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'options'


class SpaceOption(models.Model):
    space  = models.ForeignKey('spaces.Space', on_delete=models.CASCADE)
    option = models.ForeignKey('spaces.Option', on_delete=models.CASCADE)

    class Meta:
        db_table = 'space_options'


class Location(models.Model):
    space          = models.ForeignKey('spaces.Space', on_delete=models.CASCADE)
    country        = models.ForeignKey('users.Country', on_delete=models.CASCADE)
    region         = models.CharField(max_length=45)
    city           = models.CharField(max_length=20)
    address        = models.CharField(max_length=150)
    address_detail = models.CharField(max_length=45)
    latitude       = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    longitude      = models.DecimalField(max_digits=10, decimal_places=6,null=True)

    class Meta:
        db_table = 'locations'


class Image(models.Model):
    space = models.ForeignKey('spaces.Space', on_delete=models.CASCADE)
    url   = models.URLField(max_length=2000)

    class Meta:
        db_table = 'images'


class Bedroom(models.Model):
    name    = models.CharField(max_length=25, default='')
    space   = models.ForeignKey('spaces.Space', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bedrooms'


class BedroomBed(models.Model):
    bedroom  = models.ForeignKey('spaces.Bedroom', on_delete=models.CASCADE)
    bed_type = models.ForeignKey('spaces.BedType', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'bedroom_beds'


class BedType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'bed_types'


class Review(models.Model):
    space               = models.ForeignKey('spaces.Space', on_delete=models.CASCADE)
    user                = models.ForeignKey('users.User', on_delete=models.CASCADE)
    pub_date            = models.DateField(auto_now=True)
    content             = models.CharField(max_length=1000)
    cleanliness_score   = models.IntegerField(default=0)
    communication_score = models.IntegerField(default=0)
    check_in_score      = models.IntegerField(default=0)
    accuracy_score      = models.IntegerField(default=0)
    location_score      = models.IntegerField(default=0)
    value_score         = models.IntegerField(default=0)
    image_url           = models.URLField(max_length=2000)

    class Meta:
        db_table = 'reviews'


class Reservation(models.Model):
    space                    = models.ForeignKey('spaces.Space', on_delete=models.CASCADE)
    user                     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    check_in                 = models.DateField()
    check_out                = models.DateField()
    adult                    = models.IntegerField()
    children                 = models.IntegerField(null=True)
    infant                   = models.IntegerField(null=True)
    reservation_code         = models.CharField(max_length=200)
    is_work_trip             = models.BooleanField(default=0, null=True)
    trip_purpose             = models.CharField(max_length=200, null=True)
    message                  = models.CharField(max_length=1000, null=True)
    card                     = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'reservations'


class Tag(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "tags"


class SpaceTag(models.Model):
    space = models.ForeignKey('spaces.Space', on_delete=models.CASCADE)
    tag   = models.ForeignKey('spaces.Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'space_tags'

