from django.db import models

class Report(models.Model):
    generated_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='reports/')

    def __str__(self):
        return self.report_type