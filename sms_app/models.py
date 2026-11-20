from django.db import models

class SMSLog(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted to Provider'),
        ('Failed', 'Failed'),
    ]

    recipient = models.CharField(max_length=20)
    message_body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    provider_sid = models.CharField(max_length=64, blank=True, null=True)
    error_detail = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient} - {self.status} ({self.created_at:%Y-%m-%d %H:%M})"