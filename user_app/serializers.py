from rest_framework import serializers
from .models import userProfile, formData, formList
import os
key = os.getenv("ADMIN_KEY", '_admin_')

class userOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = '__all__'

class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = ['regno', 'name', 'email', 'hostel', 'block', 'room', 'number']
        
    def create(self, validated_data):
        user = validated_data['name']
        if key in user:
            validated_data['admin'] = True
            user = user.replace(key,"")
            validated_data['name'] = user
        else:
            validated_data['admin'] = False
        return userProfile.objects.create(**validated_data)

class FormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = formData
        fields = '__all__'
        
class FormListSerializer(serializers.ModelSerializer):
    class Meta:
        model = formList
        fields = '__all__'