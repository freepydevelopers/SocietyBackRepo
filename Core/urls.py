from django.urls import path
from City import views
from .views import Index, ListCityView, update_profile


urlpatterns = [
    path('', Index),
    path('city', ListCityView.as_view()),
    path('city/<int:id>/', views.details, name="citydetails"),
    path('profile/', update_profile),
]