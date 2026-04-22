from django.urls import path
from . import views

urlpatterns = [
    path('download/<int:note_id>/<int:file_no>/', views.download_note, name='download_note'),
    path('downloads/', views.view_downloads, name='view_downloads'),
    path('delete-download/<int:log_id>/', views.delete_download_log, name='delete_download_log'),
    path('notes/', views.NOTES_DETAILS, name='notes')
    
]