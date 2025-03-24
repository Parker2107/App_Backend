from django.urls import path
from .views import upload_sheet, delete_sheet, update_attendance

urlpatterns = [
    path('upload-sheet/', upload_sheet, name='upload_excel'),
    path('delete-sheet/', delete_sheet, name='delete_sheet'),
    path('edit-attendance/', update_attendance, name='edit_attendance')
]
