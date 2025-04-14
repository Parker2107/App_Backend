import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from .utils import api_key_required
from .models import SheetList, AttendanceRecord
from .serializers import SheetListSerializer, AttendanceRecordSerializer, AttendanceUpdateSerializer

@csrf_exempt
@api_view(['POST','GET'])
@api_key_required
def upload_sheet(request):
    """Handles Excel file upload, ensures unique sheet name, parses data, and stores it in the database."""
    
    if request.method == 'GET':
        sheet_name = request.GET.get("sheet_name", "").strip()
        if not sheet_name:
            return JsonResponse({"error": "Missing 'sheet_name' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        sheet = SheetList.objects.filter(sheet_name=sheet_name).first()
        if not sheet:
            return JsonResponse({"error": f"Sheet '{sheet_name}' not found."}, status=status.HTTP_404_NOT_FOUND)

        attendance_records = AttendanceRecord.objects.filter(sheet=sheet)
        serializer = AttendanceRecordSerializer(attendance_records, many=True)

        return JsonResponse({
            "sheet_name": sheet_name,
            "event_date": sheet.event_date,
            "records": serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file uploaded. Use key 'file'."}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        sheet_name = request.POST.get("sheet_name", "").strip()
        event_date = request.POST.get("event_date", "").strip()

        if not sheet_name or not event_date:
            return JsonResponse({"error": "Missing 'sheet_name' or 'event_date'."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the sheet name already exists
        if SheetList.objects.filter(sheet_name=sheet_name).exists():
            return JsonResponse({"error": f"Sheet name '{sheet_name}' already exists. Please use a unique name."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_extension = file.name.split('.')[-1].lower()
            if file_extension == 'csv':
                df = pd.read_csv(file)
            elif file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(file, engine='openpyxl')

            # Ensure required columns exist
            required_columns = ['ParticipantID', 'Participant Name', 'Attendance']
            match = (df.columns == required_columns)
            for x in match:
                if not x:
                    return JsonResponse({"error": "Invalid sheet format"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            sheet_data = {"sheet_name": sheet_name, "event_date": event_date}
            sheet_serializer = SheetListSerializer(data=sheet_data)
            
            if sheet_serializer.is_valid():
                sheet_instance = sheet_serializer.save()
            else:
                return JsonResponse({"error": "Invalid sheet data.", "details": sheet_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            # Convert DataFrame to JSON records with proper field names
            df = df.rename(columns={
                'ParticipantId': 'ParticipantId',
                'Participant Name': 'ParticipantName',
                'Attendance': 'SessionAttended'
            })

            errors = []
            valid_records = []

            for index, row in df.iterrows():
                participant_id = str(row[1]).strip()
                participant_name = str(row[0]).strip()
                session_attended = 'P'
                
                if not participant_id or not participant_name:
                    errors.append(f"Missing ParticipantId or ParticipantName at row {index + 2}. Skipping entry.")
                    continue

                valid_records.append({
                    "ParticipantId": participant_id,
                    "ParticipantName": participant_name,
                    "SessionAttended": session_attended,
                    "sheet": sheet_instance.id  # Foreign key reference
                })

            if errors:
                return JsonResponse({"error": "Some records had missing required fields.", "details": errors}, status=status.HTTP_400_BAD_REQUEST)

            # Save data using the serializer
            attendance_serializer = AttendanceRecordSerializer(data=valid_records, many=True)
            if attendance_serializer.is_valid():
                attendance_serializer.save()
                return JsonResponse({
                    "message": f"Attendance data uploaded successfully. {len(valid_records)} records saved.",
                    "sheet_name": sheet_name,
                    "event_date": event_date
                }, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({"error": "Invalid attendance data.", "details": attendance_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({"error": f"Error processing file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['DELETE'])
@api_key_required
def delete_sheet(request, sheet_name):
    """Deletes a sheet and all related attendance records."""
    try:
        sheet = SheetList.objects.filter(sheet_name=sheet_name).first()
        if not sheet:
            return JsonResponse({"error": f"Sheet '{sheet_name}' not found."}, status=status.HTTP_404_NOT_FOUND)

        sheet.delete()

        return JsonResponse({
            "message": f"Sheet '{sheet_name}' and all attendance records deleted successfully."
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({"error": f"Error deleting sheet: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@csrf_exempt
@api_view(['PATCH'])
@api_key_required
def update_attendance(request):
    """Updates attendance status for students in a specific sheet using a serializer."""
    
    sheet_name = request.data.get("sheet_name", "").strip()
    records = request.data.get("records", [])

    if not sheet_name or not records:
        return JsonResponse({"error": "Missing 'sheet_name' or 'records'."}, status=status.HTTP_400_BAD_REQUEST)

    # Get the correct sheet
    sheet = SheetList.objects.filter(sheet_name=sheet_name).first()
    if not sheet:
        return JsonResponse({"error": f"Sheet '{sheet_name}' not found."}, status=status.HTTP_404_NOT_FOUND)

    errors = []
    updated_count = 0

    for record in records:
        try:
            attendance_instance = AttendanceRecord.objects.get(ParticipantId=record["ParticipantId"], sheet=sheet)
            serializer = AttendanceUpdateSerializer(attendance_instance, data=record, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_count += 1
            else:
                errors.append(serializer.errors)

        except AttendanceRecord.DoesNotExist:
            errors.append(f"ParticipantId '{record['ParticipantId']}' not found in '{sheet_name}'.")

    return JsonResponse({
        "message": f"Attendance updated successfully. {updated_count} records modified.",
        "errors": errors
    }, status=status.HTTP_200_OK if updated_count else status.HTTP_400_BAD_REQUEST)
