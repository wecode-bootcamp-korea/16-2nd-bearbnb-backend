from django.urls  import path

from spaces.views import SpaceListView, SpaceDetailView
urlpatterns = [
    path("", SpaceListView.as_view()),
    path("/<int:space_id>", SpaceDetailView.as_view())  
]
