from django.db import models


class AttackEvent(models.Model):

    EVENT_TYPES = [
        ("SSH_BRUTE_FORCE", "SSH Brute Force"),
        ("PORT_SCAN", "Port Scan"),
        ("LOGIN_FAILURE", "Login Failure"),
    ]

    ip_address = models.GenericIPAddressField(db_index=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, db_index=True)

    username = models.CharField(max_length=100, blank=True, null=True)

    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    attempts = models.IntegerField(default=1)

    blocked = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.ip_address} - {self.event_type}"