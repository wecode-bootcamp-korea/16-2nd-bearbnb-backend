import jwt
import json
import uuid
import boto3
import random
import string
import requests
import googlemaps

from django.db.models   import Sum
from django.views       import View
from django.db          import transaction
from django.http        import JsonResponse

import my_settings
from users.models       import User, Host, Country
from spaces.models      import (
    Space, 
    Location,
    Image, 
    BedType,
    Bedroom,
    BedroomBed,
    PlaceType, 
    Property, 
    SubProperty,
    Option,
    SpaceOption,
    Tag,
    SpaceTag,
    Reservation
)
from spaces.utils       import login_required, host_required
from django.core.mail   import EmailMessage


class SpaceListView(View):
    def get(self, request):
        place_type = request.GET.get("type")
        filter_set = {}
        if place_type:
            filter_set["place_type__name"] = place_type
        spaces = Space.objects.filter(**filter_set)
            
        page            = int(request.GET.get("page", 1))
        PAGE_SIZE       = 20
        limit           = page * PAGE_SIZE
        offset          = limit - PAGE_SIZE

        results = [
        {
            "id"                : space.id,
            "name"              : space.name,
            "place_type"        : space.place_type.name,
            "city"              : [adress.city for adress in space.location_set.all()],
            "property_name"     : space.sub_property.space_property.name,
            "space_image"       : [image.url for image in space.image_set.all()],
            "max_people"        : space.max_people,
            "bedroom_quantity"  : space.bedroom_set.count(),
            "bed_quantity"      : sum([bed for bed in [bed.bedroombed_set.all().aggregate(Sum("quantity"))["quantity__sum"] for bed in space.bedroom_set.all()] if bed]),
            "bathroom_quantity" : space.bathroom,
            "space_option"      : list(set([option.option.name for option in space.spaceoption_set.all()])),
            "rating"            : space.rating,
            "price"             : space.price,
            "space_tag"         : [tag.tag.name for tag in space.spacetag_set.all()],
            "latitude"          : [adress.latitude for adress in space.location_set.all()][0],
            "longitude"         : [adress.longitude for adress in space.location_set.all()][0]
        } 
        for space in spaces[offset:limit]
        ]
        if not results:
            return JsonResponse({"message" : "SPACE_DOES_NOT_EXIST"}, status = 400)
        return JsonResponse({"results" : results}, status = 200)


class SpaceDetailView(View):
    def get(self, request, space_id):
        try:
            space   = Space.objects.get(id = space_id)
            options = [
                {"name" : option.option.name,
                 "url" : option.option.icon_url}for option in space.spaceoption_set.all()]
            room = [
            {
                "id"                : space.id,
                "name"              : space.name,
                "address"           : " ".join(map(str,[address.region for address in space.location_set.all()]+
                                                       [address.city for address in space.location_set.all()]+
                                                       [address.address for address in space.location_set.all()]+
                                                       [address.address_detail for address in space.location_set.all()])),
                "description"       : space.description,
                "space_image"       : [image.url for image in space.image_set.all()],
                "host"              : space.host.user.name,
                "host_profile"      : space.host.profile_photo,
                "propert_name"      : space.sub_property.space_property.name,
                "max_people"        : space.max_people,
                "price"             : space.price,
                "rating"            : space.rating,
                "latitude"          : [adress.latitude for adress in space.location_set.all()][0],
                "longitude"         : [adress.longitude for adress in space.location_set.all()][0],
                "bedroom"           : [
                    {
                        "name"         : room.name,
                        "bed_type"     : [bed.bed_type.name for bed in room.bedroombed_set.all()],
                        "bed_quantity" : [bed.quantity for bed in room.bedroombed_set.all()]
                    }
                    for room in space.bedroom_set.all()
                ],
                "bedroom_quantity"  : space.bedroom_set.count(),
                "bed_quantity_sum"  : sum([bed for bed in [bed.bedroombed_set.all().aggregate(Sum("quantity"))["quantity__sum"] for bed in space.bedroom_set.all()] if bed]),
                "bathroom_quantity" : space.bathroom,
                "option"            : list({value["name"]: value for value in options}.values()),
            }
            ]
            return JsonResponse({"detail_space" : room}, status = 200)
        except Space.DoesNotExist:
            return JsonResponse({"message" : "SPACE_DOES_NOT_EXIST"}, status = 400)


class HostView(View):

    @transaction.atomic
    @login_required
    def post(self, request):
        try:
            host = Host.objects.get_or_create(user=request.user)[0] 
            
            data = json.loads(request.body)
            place_type    = data["place_type"]  
            sub_property  = data["sub_property"] 
            max_people    = data["max_people"]
            bathroom      = data["bathroom"]
            is_with_host  = data["is_with_host"]
            
            country        = data["country"]
            state          = data["state"]
            city           = data["city"]
            street         = data["street"]
            address_detail = data["address_detail"] 
            bedrooms       = data["bedrooms"] # as nested dictionary
            
            # check address validity
            main_address = ' ,'.join((street, city, state, country)) 
            gmaps        = googlemaps.Client(key=my_settings.GOOGLEMAPS_KEY)
            geocoded     = gmaps.geocode(main_address, language='ko')

            if not geocoded:
                return JsonResponse({"message": "INVALID_ADDRESS"}, status=400)
 
            options      = Option.objects.filter(id__in=data["options"]) 
            place_type   = PlaceType.objects.get(id=place_type)
            sub_property = SubProperty.objects.get(id=sub_property)

            latitude           = geocoded[0]["geometry"]["location"]["lat"]
            longitude          = geocoded[0]["geometry"]["location"]["lng"]
            address_components = geocoded[0]["address_components"]

            checked_address = {
                component_type:component["long_name"] 
                    for component in address_components 
                        for component_type in component["types"]
            }
            if not checked_address.get("sublocality_level_4"):
                return JsonResponse({"message": "INVALID_ADDRESS"}, status=400)

            city = ', '.join(
                [
                    component for component in [
                         checked_address.get("sublocality_level_3"),
                         checked_address.get("sublocality_level_2"),
                         checked_address.get("sublocality_level_1"),
                         checked_address.get("locality")
                    ] if component
                ]
            )
            address = checked_address["sublocality_level_4"]    

            created_space = Space.objects.create(
                host         = host, 
                place_type   = place_type,
                sub_property = sub_property,
                max_people   = max_people, 
                bathroom     = bathroom,
                is_with_host = is_with_host
            )
            
            created_location = Location.objects.create(
                space          = created_space,
                country        = Country.objects.get(name=checked_address["country"]),
                region         = checked_address["administrative_area_level_1"],
                city           = city,
                address        = address,
                address_detail = address_detail,
                latitude       = latitude,
                longitude      = longitude 
            )
            
            for bedroom_name in bedrooms.keys():
                created_bedroom = Bedroom.objects.create(
                    name  = bedroom_name,
                    space = created_space
                )
                beds = bedrooms[bedroom_name] 

                for bed_type in beds.keys():
                    BedroomBed(
                        bedroom  = created_bedroom, 
                        bed_type = BedType.objects.get(id=bed_type),
                        quantity = beds[bed_type]
                    ).save()

            for option in options:
                SpaceOption(space=created_space, option=option).save()

            return JsonResponse(
                {
                    "message"    : "SPACE_CREATED",
                    "space_id"   : created_space.id,
                    "location_id": created_location.id
                }, 
                status=201
            )
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

 
class SpaceImagesView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = my_settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = my_settings.AWS_SECRET_ACCESS_KEY 
    )

    @transaction.atomic
    @login_required
    @host_required
    def post(self, request):
        try:
            file = request.FILES.get('space_image')
            data = json.loads(request.POST['json'])

            if not file:
                return JsonResponse({"message" : "FILE_NOT_RECIEVED"}, status=400)

            space_id = data["space_id"]
            spaces   = Space.objects.filter(id=space_id)
            
            if not spaces.exists():
                return JsonResponse({"message": "INVALID_SPACE"}, status=400)

            space      = spaces.get()
            image_uuid = str(uuid.uuid4())

            self.s3_client.upload_fileobj(
                file,
                my_settings.BUCKET,
                image_uuid,
                ExtraArgs = {
                    "ContentType": file.content_type
                }
            )
            image_url_form = (
                "https://s3.{bucket_location}.amazonaws.com/"
                "{bucket}/{uuid}"
            )
            image_url  = image_url_form.format(
                bucket_location = my_settings.BUCKET_LOCATION,
                bucket          = my_settings.BUCKET,
                uuid            = image_uuid
            )
            saved_image = Image.objects.create(space=space, url=image_url)

            return JsonResponse({
                "message"  : "IMAGE_SAVED", 
                "image_id" : saved_image.id,
                "image_url": image_url
            },status=201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)


class ReservationView(View):
    @login_required
    @transaction.atomic
    def post(self, request):
        try:
            data             = json.loads(request.body)
            space            = Space.objects.get(id=data['space'])
            reservation_code = str(uuid.uuid4())
            
            if Reservation.objects.filter(user=request.user, space=space, check_in=data['check_in'], check_out=data['check_out']).exists():
                return JsonResponse({'message':'RESERVATION_ALREADY_EXIST'}, status=400)
            if data['adult'] + data.get('children', 0) + data.get('infant', 0) > space.max_people:
                return JsonResponse({'message':f'{space.max_people}_GUESTS_MAXIMUM'}, status=400)

            Reservation(         
                space            = space,
                user             = request.user,
                check_in         = data['check_in'],
                check_out        = data['check_out'],
                adult            = data['adult'],
                children         = data.get('children'),
                infant           = data.get('infant'),
                reservation_code = reservation_code,
                is_work_trip     = data['is_work_trip'],
                trip_purpose     = data.get('trip_purpose'),
                message          = data.get('message'),
                card             = data['card'],
            ).save()

            email = EmailMessage(
                'Reservation Confirm!',
                f'Reservation Complete. Have a nice trip to {space.name}! \n Reservation code : {reservation_code}',
                to=[request.user.email])
            response = email.send()
            return JsonResponse({'message':'SUCCESS'},status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
