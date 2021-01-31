from django.urls  import path
from spaces.views import (
    SpaceListView,
    SpaceDetailView,
    HostView, 
    SpaceImagesView
)

urlpatterns = [
    path("", SpaceListView.as_view()),
    path("/<int:space_id>", SpaceDetailView.as_view()),
    path("/hosting", HostView.as_view()),
    path("/spaceimages", SpaceImagesView.as_view())
]

