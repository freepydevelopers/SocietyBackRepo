from django.urls import path
from City import views
from .views import ListCityView, Hello


urlpatterns = [
    path('', ListCityView.as_view()),
    path('<int:id>/', views.details, name="citydetails"),
    path('god/', Hello.as_view(), name="hel"),
]