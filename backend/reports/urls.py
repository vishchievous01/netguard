from django.urls import path
from . import views

urlpatterns = [
    path("timeline/", views.attack_timeline, name="attack_timeline"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/attacks/", views.api_attacks, name="api_attacks"),
    path("api/map/", views.api_attack_map, name="api_attack_map"),
]