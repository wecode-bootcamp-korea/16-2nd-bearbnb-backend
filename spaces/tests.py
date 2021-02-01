import json

from django.test        import TestCase, Client

from users.models       import User, Host, Country
from spaces.models      import (Space, Location, Image, Bedroom, 
                                BedroomBed, Property, SubProperty, 
                                BedType, Option, SpaceOption, Tag, 
                                SpaceTag, PlaceType)


client = Client()
class SpaceListViewTest(TestCase):
    def setUp(self):
        Country.objects.create(
            name = "한국"
        )
        country_id = Country.objects.get(name="한국").id

        User.objects.create(
            country_id     = country_id,
            phone          = None,
            name           = "test",
            password       = "test",
            gender         = None,
            birthdate      = None,
            email          = "test@test.com",
            profile_photo  = None,
            is_email_valid = 0
        )
        user_id = User.objects.get(name="test").id

        Host.objects.create(
            user_id       = user_id,
            profile_photo = "host_photo",
            id_card_photo = None
        )
        host_id = Host.objects.get(profile_photo="host_photo").id

        Property.objects.create(
            name = "아파트"
        )
        property_id = Property.objects.get(name="아파트").id

        SubProperty.objects.create(
            name              = "아파트",
            space_property_id = property_id
        )
        subproperty_id = SubProperty.objects.get(name="아파트").id

        PlaceType.objects.create(
            name = "다인실", 
        )
        placetype_id = PlaceType.objects.get(name="다인실").id

        Space.objects.create(
            host_id         = host_id,
            name            = "숙소이름",
            price           = "10000.00",
            description     = "숙소 설명",
            place_type_id   = placetype_id,
            sub_property_id = subproperty_id,
            max_people      = 5,
            bathroom        = 1,
            rating          = "5.00"
        )
        space_id = Space.objects.get(name="숙소이름").id

        Option.objects.create(
            name     = "와이파이",
            icon_url = "wifi_url",
        )
        option_id = Option.objects.get(name="와이파이").id

        SpaceOption.objects.create(
            space_id  = space_id,
            option_id = option_id
        )

        Location.objects.create(
            space_id       = space_id,
            country_id     = country_id,
            region         = "서울시",
            city           = "강남구",
            address        = "삼성동 테헤란로",
            address_detail = "427",
            latitude       = "37.506267",
            longitude      = "127.054067"
        )

        Image.objects.create(
            space_id = space_id,
            url      = "space_image_url"
        )
       
        BedType.objects.create(
           name   = "퀸 침대"  
        )
        bedtype_id = BedType.objects.get(name="퀸 침대").id

        Bedroom.objects.create(
           name     = "침실",
           space_id = space_id
        )
        bedroom_id = Bedroom.objects.get(name="침실").id

        BedroomBed.objects.create(
        
           bedroom_id = bedroom_id,
           bed_type_id = bedtype_id,
           quantity    = 5
        )

        Tag.objects.create(
           name = "test"
        )
        tag_id = Tag.objects.get(name="test").id

        SpaceTag.objects.create(
           space_id = space_id,
           tag_id   = tag_id 
        )

    def tearDown(self):
        Space.objects.all().delete(),
        PlaceType.objects.all().delete(),
        Property.objects.all().delete(),
        SubProperty.objects.all().delete(),
        Option.objects.all().delete(),
        SpaceOption.objects.all().delete(),
        Location.objects.all().delete(),
        Image.objects.all().delete(),
        Bedroom.objects.all().delete(),
        BedroomBed.objects.all().delete(),
        BedType.objects.all().delete(),
        Tag.objects.all().delete(),
        SpaceTag.objects.all().delete(),
        User.objects.all().delete(),
        Host.objects.all().delete(),
        Country.objects.all().delete()

    def test_get_space_list_view(self):
        response = client.get("/spaces" ,page=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
        {
    "results": [
        {
            "name": "숙소이름",
            "place_type": "다인실",
            "city": [
                "강남구"
            ],
            "property_name": "아파트",
            "space_image": [
                "space_image_url",
            ],
            "max_people": 5,
            "bedroom_quantity": 1,
            "bed_quantity": 5,
            "bathroom_quantity": 1,
            "space_option": [
                "와이파이"
            ],
            "rating": "5.00",
            "price": "10000.00",
            "space_tag": ["test"],
            "latitude": [
                "37.506267"
            ],
            "longitude": [
                "127.054067"
            ]
        }
    ]
        }
    )

    def test_get_space_list_view_keyerror(self):
        
        Space.objects.all().delete(),
        PlaceType.objects.all().delete(),
        Property.objects.all().delete(),
        SubProperty.objects.all().delete(),
        Option.objects.all().delete(),
        SpaceOption.objects.all().delete(),
        Location.objects.all().delete(),
        Image.objects.all().delete(),
        Bedroom.objects.all().delete(),
        BedroomBed.objects.all().delete(),
        BedType.objects.all().delete(),
        Tag.objects.all().delete(),
        SpaceTag.objects.all().delete(),
        User.objects.all().delete(),
        Host.objects.all().delete(),
        Country.objects.all().delete()

        response = client.get("/spaces")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"message" : "SPACE_DOES_NOT_EXIST"})
