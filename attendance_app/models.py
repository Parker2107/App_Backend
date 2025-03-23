from django.db import models
from django.core.exceptions import ValidationError

class SheetList(models.Model):
    """Stores the list of uploaded sheets with timestamps."""
    sheet_name = models.CharField(max_length=255, unique=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()

    def __str__(self):
        return self.sheet_name

class AttendanceRecord(models.Model):
    """Stores attendance details."""
    sheet = models.ForeignKey(SheetList, on_delete=models.CASCADE, related_name="attendance_records")
    ParticipantId = models.CharField(max_length=255)
    ParticipantName = models.CharField(max_length=255)
    SessionAttended = models.CharField(max_length=5,default='A')  # Should only contain 'P' or 'A'

    def __str__(self):
        return f"{self.ParticipantId} - {self.ParticipantName} ({self.SessionAttended})"
