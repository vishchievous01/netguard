from django.db import models
import json
from pathlib import Path
import subprocess
import time
from django.utils import timezone
from datetime import datetime
from core.ban_controller import ban_ip

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
    banned_at = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.ip

    def save(self, *args, **kwargs):
    if not self.banned_at:
        self.banned_at = int(time.time())

    super().save(*args, **kwargs)
    ban_ip(self.ip))

    def delete(self, *args, **kwargs):
        self._remove_from_json()
        self._remove_iptables_rule()
        super().delete(*args, **kwargs)

    def banned_at_local(self):
        if not self.banned_at:
            return None
        dt = datetime.fromtimestamp(self.banned_at, tz=timezone.get_current_timezone())
        return dt.strftime("%Y-%m-%d %H:%M:%S")