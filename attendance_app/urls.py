from django.urls import path
from .views import upload_sheet, delete_sheet, update_attendance

urlpatterns = [
    path('upload_sheet/', upload_sheet, name='upload_excel'),
    path('delete_sheet/', delete_sheet, name='delete_sheet'),
    path('edit_attendance/', update_attendance, name='edit_attendance')
]
