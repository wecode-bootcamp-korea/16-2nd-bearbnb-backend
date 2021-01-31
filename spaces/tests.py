import json
import jwt
import bcrypt

from django.test           import TestCase, Client
from unittest.mock         import patch, MagicMock

from users.models          import User, Host, Country
from spaces.models         import (Space, Location, Image, Bedroom, 
                                   BedroomBed, Property, SubProperty, 
                                   BedType, Option, SpaceOption, Tag, 
                                   SpaceTag, PlaceType)
from spaces.geocode_sample import TEHERANRO, SAMSUNGDONG
import my_settings


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
            "id":4,
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
        response = client.get('/spaces/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
        {
    "detail_space": [
       {
         "id": 2,
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
        self.assertEqual(response.json(),{"message": "SPACE_DOES_NOT_EXIST"})


class HostingTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        password = 'testpassword1'.encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        User.objects.create(
            email     = "test1@test.com",
            password  = password,
            name      = "testname",
            country   = None,
            phone     = None,
            gender    = None,
            birthdate = None 
        )
        
        test_property = Property.objects.create(name="test_property1")
        SubProperty.objects.create(
            space_property = test_property, 
            name           = "test_sub_property1"
        )

        BedType.objects.create(name="test_bedtype1")
        BedType.objects.create(name="test_bedtype2")

        Option.objects.create(name="test_option1", icon_url="http://test-url1.com")
        Option.objects.create(name="test_option2", icon_url="http://test-url2.com")

        Country.objects.create(name="대한민국")

        PlaceType.objects.create(name="test_place_type1")

    def setUp(self):
        pass

    def tearDown(self):
        Image.objects.all().delete()
        SpaceOption.objects.all().delete()
        BedroomBed.objects.all().delete()
        Bedroom.objects.all().delete()
        BedType.objects.all().delete()
        Location.objects.all().delete()
        Space.objects.all().delete()
        PlaceType.objects.all().delete()
        SubProperty.objects.all().delete()
        Property.objects.all().delete()

        Host.objects.all().delete()
        User.objects.all().delete()
        Country.objects.all().delete()

    @patch("googlemaps.Client")
    def test_temporary_hosting_login_required_fail(self, mock_gclient):
        mock_gmaps         = MagicMock()
        mock_gmaps.geocode = MagicMock(return_value=TEHERANRO)
        mock_gclient.return_value = mock_gmaps
        
        hosting = {
            "place_type"  : 1,
            "sub_property": 2,
            "max_people"  : 5,
            "bathroom"    : 3,
            "is_with_host": True,
            "country"     : "대한민국",
            "state"       : "서울특별시",
            "city"        : "강남구",
            "street"      : "테헤란로",
            "bedrooms"    : {
                "1번 침실" : {
                    1: 3,
                    2: 2
                },
                "2번 침실" : {
                    1: 1,
                    1: 4 
                }
            },
            "options"       : [1, 2],
            "address_detail": "테스트빌딩1" 
        }
        response = client.post(
            '/spaces/hosting', 
            json.dumps(hosting), 
            content_type = 'application/json'
        )
        self.assertEqual(
            response.json(),
            {
                'message': 'LOGIN_REQUIRED'
            }
        )
        self.assertEqual(response.status_code, 401)

    @patch("googlemaps.Client")
    def test_temporary_hosting_invalid_user_fail(self, mock_gclient):
        mock_gmaps         = MagicMock()
        mock_gmaps.geocode = MagicMock(return_value=TEHERANRO)
        mock_gclient.return_value = mock_gmaps

        token = jwt.encode(
            {'id': 400}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization": token}
        
        hosting = {
            "place_type"  : 1,
            "sub_property": 1,
            "max_people"  : 5,
            "bathroom"    : 3,
            "is_with_host": True,
            "country"     : "대한민국",
            "state"       : "서울특별시",
            "city"        : "강남구",
            "street"      : "테헤란로",
            "bedrooms"    : {
                "1번 침실" : {
                    1: 3,
                    2: 2
                },
                "2번 침실" : {
                    1: 1,
                    2: 4 
                }
            },
            "options"        : [1, 2],
            "address_detail" : "테스트빌딩1" 
        }
        response = client.post(
            '/spaces/hosting', 
            json.dumps(hosting), 
            **headers,
            content_type = 'application/json'
        )
        self.assertEqual(
            response.json(),
            {
                'message': 'INVALID_USER',
            }
        )
        self.assertEqual(response.status_code, 401)

    @patch("googlemaps.Client")
    def test_temporary_hosting_post_jwt_decode_fail(self, mock_gclient):
        mock_gmaps         = MagicMock()
        mock_gmaps.geocode = MagicMock(return_value=TEHERANRO)
        mock_gclient.return_value = mock_gmaps

        headers = {"HTTP_Authorization": "invalid_token_form"}
        
        hosting = {
            "place_type"  : 1,
            "sub_property": 1,
            "max_people"  : 5,
            "bathroom"    : 3,
            "is_with_host": True,
            "country"     : "대한민국",
            "state"       : "서울특별시",
            "city"        : "강남구",
            "street"      : "테헤란로",
            "bedrooms"    : {
                "1번 침실" : {
                    "test_bedtype1": 3,
                    "test_bedtype2": 2
                },
                "2번 침실" : {
                    "test_bedtype1": 1,
                    "test_bedtype2": 4 
                }
            },
            "options"        : [1, 2],
            "address_detail" : "테스트빌딩1" 
        }
        response = client.post(
            '/spaces/hosting', 
            json.dumps(hosting), 
            **headers,
            content_type = 'application/json'
        )
        self.assertEqual(
            response.json(),
            {
                'message': 'JWT_DECODE_ERROR',
            }
        )
        self.assertEqual(response.status_code, 400)

    @patch("googlemaps.Client")
    def test_temporary_hosting_post_invalid_address_fail(self, mock_gclient):
        mock_gmaps         = MagicMock()
        mock_gmaps.geocode = MagicMock(return_value=[])
        mock_gclient.return_value = mock_gmaps

        user  = User.objects.get(email="test1@test.com")
        token = jwt.encode(
            {'id': user.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization": token}
        
        hosting = {
            "place_type"  : 1,
            "sub_property": 1,
            "max_people"  : 5,
            "bathroom"    : 3,
            "is_with_host": True,
            "country"     : "존재하지않는주소",
            "state"       : "존재하지않는주소",
            "city"        : "존재하지않는주소",
            "street"      : "존재하지않는주소",
            "bedrooms"    : {
                "1번 침실" : {
                    1: 3,
                    2: 2
                },
                "2번 침실" : {
                    1: 1,
                    2: 4 
                }
            },
            "options"       : [1, 2],
            "address_detail": "테스트빌딩1" 
        }
        response = client.post(
            '/spaces/hosting', 
            json.dumps(hosting), 
            **headers,
            content_type = 'application/json'
        )
        self.assertEqual(
            response.json(),
            {
                'message'    : 'INVALID_ADDRESS',
            }
        )
        self.assertEqual(response.status_code, 400)

    @patch("googlemaps.Client")
    def test_temporary_hosting_post_no_sublocal_level4_fail(self, mock_gclient):
        mock_gmaps         = MagicMock()
        mock_gmaps.geocode = MagicMock(return_value=SAMSUNGDONG)
        mock_gclient.return_value = mock_gmaps

        user  = User.objects.get(email="test1@test.com")
        token = jwt.encode(
            {'id': user.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization": token}
        
        hosting = {
            "place_type"  : 1,
            "sub_property": 1,
            "max_people"  : 5,
            "bathroom"    : 3,
            "is_with_host": True,
            "country"     : "대한민국",
            "state"       : "서울특별시",
            "city"        : "강남구",
            "street"      : "테헤란로",
            "bedrooms"    : {
                "1번 침실" : {
                    1: 3,
                    2: 2
                },
                "2번 침실" : {
                    1: 1,
                    2: 4 
                }
            },
            "options"       : [1, 2],
            "address_detail": "테스트빌딩1" 
        }
        response = client.post(
            '/spaces/hosting', 
            json.dumps(hosting), 
            **headers,
            content_type = 'application/json'
        )

        self.assertEqual(
            response.json(),
            {
                'message': 'INVALID_ADDRESS',
            }
        )
        self.assertEqual(response.status_code, 400)

    @patch("googlemaps.Client")
    def test_temporary_hosting_key_error(self, mock_gclient):
        mock_gmaps         = MagicMock()
        mock_gmaps.geocode = MagicMock(return_value=TEHERANRO)
        mock_gclient.return_value = mock_gmaps

        user  = User.objects.get(email="test1@test.com")
        token = jwt.encode(
            {'id': user.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization": token}
        
        hosting = {
            "place_type"  : 1,
            "sub_property": 1,
            "max_people"  : 5,
            "bathroom"    : 3,
            "is_with_host": True,
            "bedrooms"    : {
                "1번 침실" : {
                    1: 3,
                    2: 2
                },
                "2번 침실" : {
                    1: 1,
                    2: 4 
                }
            },
            "options"       : [1, 2],
            "address_detail": "테스트빌딩1" 
        }
        response = client.post(
            '/spaces/hosting', 
            json.dumps(hosting), 
            **headers,
            content_type = 'application/json'
        )

        self.assertEqual(
            response.json(),
            {
                'message': 'KEY_ERROR',
            }
        )
        self.assertEqual(response.status_code, 400)

    @patch("googlemaps.Client")
    def test_temporary_hosting_post_success(self, mock_gclient):
        mock_gmaps         = MagicMock()
        mock_gmaps.geocode = MagicMock(return_value=TEHERANRO)
        mock_gclient.return_value = mock_gmaps

        user  = User.objects.get(email="test1@test.com")
        token = jwt.encode(
            {'id': user.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization": token}
        
        hosting = {
            "place_type"  : 1,
            "sub_property": 1,
            "max_people"  : 5,
            "bathroom"    : 3,
            "is_with_host": True,
            "country"     : "대한민국",
            "state"       : "서울특별시",
            "city"        : "강남구",
            "street"      : "테헤란로",
            "bedrooms"    : {
                "1번 침실" : {
                    1: 3,
                    2: 2
                },
                "2번 침실" : {
                    1: 1,
                    2: 4 
                }
            },
            "options"        : [1, 2],
            "address_detail" : "테스트빌딩1" 
        }
        response = client.post(
            '/spaces/hosting', 
            json.dumps(hosting), 
            **headers,
            content_type = 'application/json'
        )

        self.assertEqual(
            response.json(),
            {
                'message'    : 'SPACE_CREATED',
                'space_id'   : 1,
                'location_id': 1
            }
        )
        self.assertEqual(response.status_code, 201)


class SpacePictureTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        password = 'testpassword1'.encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

        testuser1 = User.objects.create(
            email     = "test1@test.com",
            password  = password,
            name      = "testname",
            country   = None,
            phone     = None,
            gender    = None,
            birthdate = None 
        )
        testuser2 = User.objects.create(
            email     = "test2@test.com",
            password  = password,
            name      = "testname",
            country   = None,
            phone     = None,
            gender    = None,
            birthdate = None 
        )
        testhost1 = Host.objects.create(
            user = testuser1
        )
        
        test_property      = Property.objects.create(name="test_property1")
        test_sub_property1 = SubProperty.objects.create(
            space_property = test_property, 
            name           = "test_sub_property1"
        )
        test_place_type1   = PlaceType.objects.create(name="test_place_type1")

        Space.objects.create(
            host         = testhost1, 
            place_type   = test_place_type1,
            sub_property = test_sub_property1,
            max_people   = 4, 
            bathroom     = 3,
            is_with_host = True
        )

    def setUp(self):
        pass

    def tearDown(self):
        Image.objects.all().delete()
        Space.objects.all().delete()
        PlaceType.objects.all().delete()
        SubProperty.objects.all().delete()
        Property.objects.all().delete()

        Host.objects.all().delete()
        User.objects.all().delete()

    @patch('spaces.views.SpaceImagesView.s3_client.upload_fileobj')
    def test_space_image_post_host_required_fail(self, mock_boto3_client):
        mock_boto3_client.upload_fileobj = MagicMock() 

        testuser2 = User.objects.get(email= "test2@test.com")
        token = jwt.encode(
            {'id': testuser2.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization" : token}
        
        space_info = {
            "space_id": 1
        } 

        form = {
            "space_image": open("../test_picture.png", 'rb'),
            "json"       : json.dumps(space_info)
        }

        image_url_form = (
            "https://s3.{bucket_location}.amazonaws.com/"
            "{bucket}/{space_image}"
        )
        success_image_url = image_url_form.format(
            bucket_location = my_settings.BUCKET_LOCATION,
            bucket          = my_settings.BUCKET,
            space_image     = "test_picture.png" 
        )

        response = client.post(
            '/spaces/spaceimages', 
            data = form, 
            **headers,
        )
        self.assertEqual(
            response.json(), 
            {
                'message'  : 'INVALID_HOST',
            }
        )
        self.assertEqual(response.status_code, 401)

    @patch('spaces.views.SpaceImagesView.s3_client.upload_fileobj')
    def test_space_image_post_jwt_decode_error(self, mock_boto3_client):
        testuser1 = User.objects.get(email= "test1@test.com")
        token = jwt.encode(
            {'id': testuser1.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization" : "WEIRD_TOKEN"}
        
        space_info = {
            "space_id": Space.objects.get(
                host=Host.objects.get(user=testuser1)
            ).id
        } 

        form = {
            "space_image": open("../test_picture.png", 'rb'),
            "json"       : json.dumps(space_info)
        }

        image_url_form = (
            "https://s3.{bucket_location}.amazonaws.com/"
            "{bucket}/{space_image}"
        )
        success_image_url = image_url_form.format(
            bucket_location = my_settings.BUCKET_LOCATION,
            bucket          = my_settings.BUCKET,
            space_image     = "test_picture.png" 
        )

        response = client.post(
            '/spaces/spaceimages', 
            data = form, 
            **headers,
        )
        self.assertEqual(
            response.json(), 
            {
                'message'  : 'JWT_DECODE_ERROR',
            }
        )
        self.assertEqual(response.status_code, 400)

    @patch('spaces.views.SpaceImagesView.s3_client.upload_fileobj')
    def test_space_image_post_file_not_recieved(self, mock_boto3_client):
        testuser1 = User.objects.get(email= "test1@test.com")
        token = jwt.encode(
            {'id': testuser1.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization": token}
        
        space_info = {
            "space_id": Space.objects.get(
                host=Host.objects.get(user=testuser1)
            ).id
        } 

        form = {
            "json": json.dumps(space_info)
        }

        image_url_form = (
            "https://s3.{bucket_location}.amazonaws.com/"
            "{bucket}/{space_image}"
        )
        success_image_url = image_url_form.format(
            bucket_location = my_settings.BUCKET_LOCATION,
            bucket          = my_settings.BUCKET,
            space_image     = "test_picture.png" 
        )

        response = client.post(
            '/spaces/spaceimages', 
            data = form, 
            **headers,
        )
        self.assertEqual(
            response.json(), 
            {
                'message': 'FILE_NOT_RECIEVED',
            }
        )
        self.assertEqual(response.status_code, 400)

    @patch('spaces.views.SpaceImagesView.s3_client.upload_fileobj')
    def test_space_image_post_invalid_space(self, mock_boto3_client):
        testuser1 = User.objects.get(email= "test1@test.com")
        token = jwt.encode(
            {'id': testuser1.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization": token}
        
        space_info = {
            "space_id": 400
        } 

        form = {
            "space_image": open("../test_picture.png", 'rb'),
            "json"       : json.dumps(space_info)
        }

        image_url_form = (
            "https://s3.{bucket_location}.amazonaws.com/"
            "{bucket}/{space_image}"
        )
        success_image_url = image_url_form.format(
            bucket_location = my_settings.BUCKET_LOCATION,
            bucket          = my_settings.BUCKET,
            space_image     = "test_picture.png" 
        )

        response = client.post(
            '/spaces/spaceimages', 
            data = form, 
            **headers,
        )
        self.assertEqual(
            response.json(), 
            {
                'message': 'INVALID_SPACE',
            }
        )
        self.assertEqual(response.status_code, 400)

    @patch('spaces.views.SpaceImagesView.s3_client.upload_fileobj')
    def test_space_image_post_key_error(self, mock_boto3_client):
        testuser1 = User.objects.get(email="test1@test.com")
        token = jwt.encode(
            {'id': testuser1.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization": token}
        
        space_info = {
        } 

        form = {
            "space_image": open("../test_picture.png", 'rb'),
            "json"       : json.dumps(space_info)
        }

        image_url_form = (
            "https://s3.{bucket_location}.amazonaws.com/"
            "{bucket}/{space_image}"
        )
        success_image_url = image_url_form.format(
            bucket_location = my_settings.BUCKET_LOCATION,
            bucket          = my_settings.BUCKET,
            space_image     = "test_picture.png" 
        )

        response = client.post(
            '/spaces/spaceimages', 
            data = form, 
            **headers,
        )
        self.assertEqual(
            response.json(), 
            {
                'message': 'KEY_ERROR',
            }
        )
        self.assertEqual(response.status_code, 400)

    @patch('uuid.uuid4')
    @patch('spaces.views.SpaceImagesView.s3_client.upload_fileobj')
    def test_space_image_post_success(self, mock_boto3_client, mock_uuid4):
        mocked_uuid             = "ebec2cfc-8edf-4a69-8ddf-bbf6490f63d8"
        mock_uuid4.return_value = mocked_uuid 
        testuser1 = User.objects.get(email="test1@test.com")
        token = jwt.encode(
            {'id': testuser1.id}, 
            my_settings.SECRET_KEY, 
            algorithm = my_settings.ALGORITHM
        )
        headers = {"HTTP_Authorization": token}
        
        space_info = {
            "space_id": Space.objects.get(
                host=Host.objects.get(user=testuser1)
            ).id
        } 

        form = {
            "space_image": open("../test_picture.png", 'rb'),
            "json"       : json.dumps(space_info)
        }

        image_url_form = (
            "https://s3.{bucket_location}.amazonaws.com/"
            "{bucket}/{uuid}"
        )
        success_image_url = image_url_form.format(
            bucket_location = my_settings.BUCKET_LOCATION,
            bucket          = my_settings.BUCKET,
            uuid            = mocked_uuid 
        )

        response = client.post(
            '/spaces/spaceimages', 
            data = form, 
            **headers,
        )
        self.assertEqual(
            response.json(), 
            {
                'message'  : 'IMAGE_SAVED',
                'image_id' : 5,
                'image_url': success_image_url
            }
        )
        self.assertEqual(response.status_code, 201)
