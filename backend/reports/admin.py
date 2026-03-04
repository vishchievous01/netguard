from django.contrib import admin
from .models import AttackEvent


@admin.register(AttackEvent)
class AttackEventAdmin(admin.ModelAdmin):

    list_display = (
        "timestamp",
        "ip_address",
        "event_type",
        "username",
        "attempts",
        "blocked",
    )

    list_filter = ("event_type", "blocked")
    search_fields = ("ip_address", "username")