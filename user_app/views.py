from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db import connection
from .forms import NSForm
from .models import userProfile, formData, formList
from .serializers import userProfileSerializer, FormDataSerializer, userOutputSerializer, FormListSerializer
from .utils import api_key_required
from datetime import datetime, time
from django.views.decorators.csrf import csrf_exempt
import pytz

last_time = time(hour=16, minute=0, second=0)

def keep_alive(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "ok"}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@api_key_required
def indexAll(request):
    if request.method == 'GET':
        users = userProfile.objects.all()
        serializer = userOutputSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = userProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_key_required
@api_view(['GET'])
def check(request):
    if request.method == 'GET':
        email = request.headers.get("email")
        try:
            user = userProfile.objects.get(email=email)
        except:
            return Response({'error': 'Registration Number not found, Invalid User'}, status=status.HTTP_404_NOT_FOUND)
        serializer = userOutputSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_key_required
@api_view(['GET', 'DELETE'])
def deleteID(request, user_id):
    if request.method == 'GET':
        users = userProfile.objects.get(regno=user_id)
        serializer = userOutputSerializer(users)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        user = userProfile.objects.get(regno=user_id)
        user.delete()
        return Response({'message': f'{user_id} Profile deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_key_required
@api_view(['GET', 'DELETE'])
def delete(request):
    if request.method == 'GET':
        users = userProfile.objects.all()
        serializer = userOutputSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        userProfile.objects.all().delete()
        return Response({'message': 'All profiles deleted'}, status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_key_required
@api_view(['GET', 'PUT', 'PATCH'])
def edit(request, user_id):
    if request.method == 'GET':
        try:
            user = userProfile.objects.get(regno=user_id)
        except:
            return Response({'error': 'Registration Number not found, Invalid User'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = userProfileSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        try:
            user = userProfile.objects.get(regno=user_id)
        except:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = userProfileSerializer(instance=user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        try:
            user = userProfile.objects.get(regno=user_id)
        except:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = userProfileSerializer(instance=user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def create_new_form():
    dt = datetime.now().date()
    form_name = "NS for "+dt.strftime("%Y-%m-%d")
    data = {'form_name': form_name}
    serializer = FormListSerializer(data=data)

    if serializer.is_valid():
        new_form = serializer.save()
        return new_form
    else:
        raise ValueError(serializer.errors)
    
@csrf_exempt
@api_key_required
@api_view(['GET', 'POST'])
def formUpload(request):
    if request.method == "POST":
        data_c = request.data.copy()
        latest_form = formList.objects.order_by('-form_date').first()
        today = datetime.now().date()
        ist = pytz.timezone('Asia/Kolkata')
        time = datetime.now(tz=ist).time()
        
        #if time>last_time:
            #return Response({"message": "Deadline for applying to NS is over"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if latest_form:
            form_date = latest_form.form_date.date()

            if today == form_date:
                data_c['NS'] = latest_form.id
            else:
                new_form = create_new_form()
                data_c['NS'] = new_form.id
        else:
            new_form = create_new_form()
            data_c['NS'] = new_form.id
        
        serializer = FormDataSerializer(data=data_c)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Form uploaded successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "GET":
        form_entries = formData.objects.all()
        serializer = FormDataSerializer(form_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

@api_key_required
@api_view(['GET'])
def getNSForm(request, name):
    list = name.split("-")
    x = datetime(int(list[0]), int(list[1], list[2]))
    print(x)
    form = formList.objects.get(form_date=x)
    print(form)
    id = form.id
    formdata = formData.objects.get(NS=id)
    serializer = FormDataSerializer(formdata, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
        