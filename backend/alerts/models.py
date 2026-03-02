from django.db import models
import json
from pathlib import Path
import subprocess
import time
from django.utils import timezone
from datetime import datetime

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

        self._write_to_json()
        self._apply_iptables_rule()

    def delete(self, *args, **kwargs):
        self._remove_from_json()
        self._remove_iptables_rule()
        super().delete(*args, **kwargs)

    def _write_to_json(self):
        json_path = Path("/home/netguard/netguard/db/bans.json")

        if json_path.exists():
            with open(json_path, "r") as f:
                data = json.load(f)
        else:
            data = {"banned_ips": [], "whitelisted_ips": []}

        # Remove existing entry
        data["banned_ips"] = [
            entry for entry in data["banned_ips"]
            if entry["ip"] != self.ip
        ]

        data["banned_ips"].append({
            "ip": self.ip,
            "banned_at": self.banned_at
        })

        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)

    def _remove_from_json(self):
        json_path = Path("/home/netguard/netguard/db/bans.json")

        if not json_path.exists():
            return

        with open(json_path, "r") as f:
            data = json.load(f)

        data["banned_ips"] = [
            entry for entry in data["banned_ips"]
            if entry["ip"] != self.ip
        ]

        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)

    def _apply_iptables_rule(self):
        subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-s", self.ip, "-j", "DROP"]
        )

    def _remove_iptables_rule(self):
        subprocess.run(
            ["sudo", "iptables", "-D", "INPUT", "-s", self.ip, "-j", "DROP"]
        )

    def banned_at_local(self):
        if not self.banned_at:
            return None
        dt = datetime.fromtimestamp(self.banned_at, tz=timezone.get_current_timezone())
        return dt.strftime("%Y-%m-%d %H:%M:%S")