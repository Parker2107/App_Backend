from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db import connection
from .forms import NSForm
from .models import userProfile, formData
from .serializers import userProfileSerializer, FormDataSerializer, userOutputSerializer
from .utils import api_key_required

def keep_alive(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "ok"}, status=status.HTTP_200_OK)

@api_key_required
@api_view(['GET', 'POST'])
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

@api_key_required
@api_view(['GET'])
def check(request,user_id):
    if request.method == 'GET':
        try:
            user = userProfile.objects.get(regno=user_id)
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
    
@api_key_required
@api_view(['GET', 'POST'])
def formUpload(request):
    if request.method == "POST":
        serializer = FormDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Form uploaded successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "GET":
        form_entries = formData.objects.all()
        serializer = FormDataSerializer(form_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
        