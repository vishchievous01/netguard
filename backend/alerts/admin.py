from django.contrib import admin
from .models import Alert, BannedIP

@admin.register(BannedIP)
class BannedIPAdmin(admin.ModelAdmin):
    list_display = ("ip", "banned_at")

    def changelist_view(self, request, extra_context=None):
        BannedIP.sync_from_json()
        return super().changelist_view(request, extra_context)

admin.site.register(Alert)