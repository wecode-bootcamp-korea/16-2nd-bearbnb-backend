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
        country = Country.objects.create(
            name = "한국"
        )

        user = User.objects.create(
            country_id     = country.id,
            phone          = None,
            name           = "test",
            password       = "test",
            gender         = None,
            birthdate      = None,
            email          = "test@test.com",
            profile_photo  = None,
            is_email_valid = 0
        )

        host = Host.objects.create(
            user_id       = user.id,
            profile_photo = "host_photo",
            id_card_photo = "id_card_url"
        )

        space_property = Property.objects.create(
            name = "아파트"
        )

        subProperty = SubProperty.objects.create(
            name              = "아파트",
            space_property_id = space_property.id
        )

        placeType = PlaceType.objects.create(
            name  = "다인실", 
        )

        space = Space.objects.create(
            host_id         = host.id,
            name            = "숙소이름",
            price           = "10000.00",
            description     = "숙소 설명",
            place_type_id   = placeType.id,
            sub_property_id = subProperty.id,
            max_people      = 5,
            bathroom        = 1,
            rating          = "5.00"
        )

        option = Option.objects.create(
            name     = "와이파이",
            icon_url = "wifi_url",
        )

        spaceOption = SpaceOption.objects.create(
            space_id  = space.id,
            option_id = option.id
        )

        locaion = Location.objects.create(
            space_id       = space.id,
            country_id     = country.id,
            region         = "서울시",
            city           = "강남구",
            address        = "삼성동 테헤란로",
            address_detail = "427",
            latitude       = "37.506267",
            longitude      = "127.054067"
        )

        image = Image.objects.create(
            space_id = space.id,
            url      = "space_image_url"
        )
       
        bedType = BedType.objects.create(
           name   = "퀸 침대"  
        )

        bedroom = Bedroom.objects.create(
           name     = "침실",
           space_id = space.id
        )

        bedRoom = BedroomBed.objects.create(
        
           bedroom_id  = bedroom.id,
           bed_type_id = bedType.id,
           quantity    = 5
        )

        tag = Tag.objects.create(
           name = "test"
        )

        spaceTag = SpaceTag.objects.create(
           space_id = space.id,
           tag_id   = tag.id 
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
            "id":3,
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
            "latitude": ["37.506267"],
            "longitude": ["127.054067"]
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


client = Client()
class SpaceDetailViewTest(TestCase):
    def setUp(self):
        country = Country.objects.create(
            name = "한국"
        )

        user = User.objects.create(
            country_id     = country.id,
            phone          = None,
            name           = "test",
            password       = "test",
            gender         = None,
            birthdate      = None,
            email          = "test@test.com",
            profile_photo  = None,
            is_email_valid = 0
        )

        host = Host.objects.create(
            user_id       = user.id,
            profile_photo = "host_photo",
            id_card_photo = "id_card_url"
        )

        space_property = Property.objects.create(
            name = "아파트"
        )

        subProperty = SubProperty.objects.create(
            name              = "아파트",
            space_property_id = space_property.id
        )

        placeType = PlaceType.objects.create(
            name  = "다인실", 
        )

        space = Space.objects.create(
            host_id         = host.id,
            name            = "숙소이름",
            price           = "10000.00",
            description     = "숙소 설명",
            place_type_id   = placeType.id,
            sub_property_id = subProperty.id,
            max_people      = 5,
            bathroom        = 1,
            rating          = "5.00"
        )

        option = Option.objects.create(
            name     = "와이파이",
            icon_url = "wifi_url",
        )

        spaceOption = SpaceOption.objects.create(
            space_id  = space.id,
            option_id = option.id
        )

        locaion = Location.objects.create(
            space_id       = space.id,
            country_id     = country.id,
            region         = "서울시",
            city           = "강남구",
            address        = "삼성동 테헤란로",
            address_detail = "427",
            latitude       = "37.506267",
            longitude      = "127.054067"
        )

        image = Image.objects.create(
            space_id = space.id,
            url      = "space_image_url"
        )
       
        bedType = BedType.objects.create(
           name   = "퀸 침대"  
        )

        bedroom = Bedroom.objects.create(
           name     = "침실",
           space_id = space.id
        )

        bedRoom = BedroomBed.objects.create(
        
           bedroom_id  = bedroom.id,
           bed_type_id = bedType.id,
           quantity    = 5
        )

        tag = Tag.objects.create(
           name = "test"
        )

        spaceTag = SpaceTag.objects.create(
           space_id = space.id,
           tag_id   = tag.id 
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

    def test_get_space_detail_view(self):
        response = client.get('/spaces/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
    "detail_space": [
       {
         "id": 1,
         "name": "숙소이름",
         "address": "서울시 강남구 삼성동 테헤란로 427",
         "description": "숙소 설명",
         "space_image": [
           "space_image_url"
         ],
         "host": "test",
         "host_profile": "host_photo",
         "propert_name": "아파트",
         "max_people": 5,
         "price": "10000.00",
         "rating": "5.00",
         "latitude": "37.506267",
         "longitude": "127.054067",
         "bedroom": [
           {
             "name": "침실",
             "bed_type": [
               "퀸 침대"
             ],
             "bed_quantity": [
               5
             ]
           }
         ],
         "bedroom_quantity": 1,
         "bed_quantity_sum": 5,
         "bathroom_quantity": 1,
         "option": [
           {
             "name": "와이파이",
             "url": "wifi_url"
           }
         ]
       }
     ]
}

    )  

    def test_get_space_detail_view_error(self):
        response = client.get("/spaces/3333")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"message" : "SPACE_DOES_NOT_EXIST"})