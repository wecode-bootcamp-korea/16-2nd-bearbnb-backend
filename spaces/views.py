import json

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Sum

from spaces.models      import (Space, Location, Image, Bedroom, BedroomBed, 
                                Option, SpaceOption, Tag, SpaceTag, PlaceType)


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
            "latitude"          : [adress.latitude for adress in space.location_set.all()],
            "longitude"         : [adress.longitude for adress in space.location_set.all()]
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