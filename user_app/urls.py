from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexAll, name="indexAll"),
    path("register/", views.indexAll, name="register"),
    path("check/<str:user_id>/", views.check, name="check"),
    path("delete/<str:user_id>/",views.deleteID, name="delete"),
    path("delete/",views.delete, name="delete"),
    path("edit/<str:user_id>/", views.edit, name="edit"),
    path("upload-form/", views.formUpload, name="form"),
    path("get-form/<str:name>/",views.getNSForm, name="getNSForm"),
    path("keep-alive/", views.keep_alive, name="keep_alive")
]
