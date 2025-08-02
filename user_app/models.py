from django.db import models

class userProfile(models.Model):
    regno = models.CharField(max_length=9, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    hostel = models.CharField(max_length=5)
    block = models.CharField(max_length=5)
    room = models.CharField(max_length=5)
    number = models.CharField(max_length=15, unique=True)
    admin = models.BooleanField(default=False)
    user_create_datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id} - {self.name} - {self.regno}"
    
class formList(models.Model):
    form_name = models.TextField()
    form_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.form_name

class formData(models.Model):
    regno = models.CharField(max_length=9)
    name = models.CharField(max_length=50)
    domain = models.TextField()
    NS = models.ForeignKey(formList, on_delete=models.CASCADE, related_name="NS_form_key", default=0)
    
    def __str__(self):
        return f"{self.regno}"

    