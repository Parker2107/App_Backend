from rest_framework import serializers
from rest_framework import serializers
from .models import SheetList, AttendanceRecord

class SheetListSerializer(serializers.ModelSerializer):
    """Serializes sheet metadata (name and event date)."""
    event_date = serializers.DateField()

    class Meta:
        model = SheetList
        fields = ['sheet_name', 'upload_date', 'event_date']

class AttendanceRecordSerializer(serializers.ModelSerializer):
    """Serializes attendance data linked to a sheet."""
    class Meta:
        model = AttendanceRecord
        fields = ['ParticipantId', 'ParticipantName', 'SessionAttended', 'sheet']

    def validate_SessionAttended(self, value):
        """Ensure the attendance status is either 'P' (Present) or 'A' (Absent)."""
        if value not in ['P', 'A']:
            raise serializers.ValidationError("SessionAttended must be 'P' or 'A'.")
        return value

class AttendanceUpdateSerializer(serializers.ModelSerializer):
    """Serializer to validate and update attendance records."""
    
    class Meta:
        model = AttendanceRecord
        fields = ["ParticipantId", "ParticipantName", "SessionAttended"]

    def update(self, instance, validated_data):
        """Update an existing attendance record."""
        instance.SessionAttended = validated_data.get("SessionAttended", instance.SessionAttended)
        instance.save()
        return instance
