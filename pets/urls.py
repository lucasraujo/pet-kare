from django.urls import path
from .views import PetsView
from .views import PetsViewWhithId

urlpatterns = [
    path('pets/', PetsView.as_view()),
    path('pets/<int:pet_id>/', PetsViewWhithId.as_view())
]