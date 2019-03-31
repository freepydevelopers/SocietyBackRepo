from django.urls import path
from City import views
from .views import Index, ListCityView, Hello, update_profile


urlpatterns = [
    path('', Index),
    path('city', ListCityView.as_view()),
    path('city/<int:id>/', views.details, name="citydetails"),
    path('god/', Hello.as_view(), name="hel"),
    path('profile/', update_profile),
]