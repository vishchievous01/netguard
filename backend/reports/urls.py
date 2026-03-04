from django.urls import path
from .views import attack_timeline, dashboard, api_attacks

urlpatterns = [
    path("timeline/", attack_timeline, name="attack_timeline"),
    path("dashboard/", dashboard, name="dashboard"),
    path("api/attacks/", api_attacks, name="api_attacks"),
]