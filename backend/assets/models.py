from django.db import models

class Asset(models.Model):
    hostname = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    operating_system = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hostname