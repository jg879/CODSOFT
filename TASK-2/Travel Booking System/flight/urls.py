from django.urls import path
from flight.views import *


urlpatterns = [
    path("", index, name="index"),
    path("query/places/<str:q>", query, name="query"),
    path("search",search,name="search"),
    path("review",review,name="review"),
    path('success/',success,name = "success"),
] 
