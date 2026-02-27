from django.db import models

class LogEntry(models.Model):
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE)
    log_level = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.asset.hostname} - {self.log_level}"