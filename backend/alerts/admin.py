from django.contrib import admin
from .models import Alert, BannedIP


@admin.register(BannedIP)
class BannedIPAdmin(admin.ModelAdmin):
    list_display = ("ip", "banned_at_local")
    readonly_fields = ("banned_at",)


admin.site.register(Alert)