from django.urls import path
from .views import *

urlpatterns = [
    path("", main, name="main"),
    path("search",search_hotels,name="search_hotel"),
    path("review",review_hotel,name="review_hotel"),
    path("payment",hotel_payment,name="hotel_payment"),
    path("success/",success,name="success"),
]