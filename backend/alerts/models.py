from django.db import models
import json
from pathlib import Path
from django.conf import settings

class Alert(models.Model):
    SEVERITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BannedIP(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    banned_at = models.BigIntegerField()

    def __str__(self):
        return self.ip

    @staticmethod
    def sync_from_json():
        json_path = Path("/home/netguard/netguard/db/bans.json")

        if not json_path.exists():
            return

        with open(json_path, 'r') as f:
            data = json.load(f)
        
        banned_ips = data.get("banned_ips", [])

        for entry in banned_ips:
            BannedIP.objects.update_or_create(
                ip=entry["ip"],
                defaults={"banned_at": entry["banned_at"]}
            )