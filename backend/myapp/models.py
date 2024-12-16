from django.db import models

class MobileData(models.Model):
    key = models.CharField(max_length=100)
    data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.key} - {self.data} at {self.timestamp}"
