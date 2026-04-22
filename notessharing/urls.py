from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Admin
    path('admin/', admin.site.urls),

    # Main Pages
    path('', views.Index, name='index'),
    path('base/', views.BASE, name='base'),

    # Auth
    path('login/', views.LOGIN, name='login'),
    path('dologin/', views.doLogin, name='doLogin'),
    path('logout/', views.doLogout, name='logout'),
    path('usersignup/', views.USERSIGNUP, name='usersignup'),

    # User
    path('profile/', views.PROFILE, name='profile'),
    path('password/', views.CHANGE_PASSWORD, name='change_password'),

    # Notes (Main App Views)
    path('notes/', views.NOTES_DETAILS, name='notes_details'),
    path('dashboard/', views.DASHBOARD, name='dashboard'),

    # Notes Management
    path('add-notes/', views.ADD_NOTES, name='add_notes'),
    path('manage-notes/', views.MANAGE_NOTES, name='manage_notes'),
    path('delete-notes/<str:id>/', views.DELETE_NOTES, name='delete_notes'),
    path('view-notes/<str:id>/', views.VIEW_NOTES, name='view_notes'),
    path('edit-notes/', views.EDIT_NOTES, name='edit_notes'),
    path('search-notes/', views.SEARCH_NOTES, name='search_notes'),

    # 🔥 IMPORTANT (nssapp URLs)
    path('', include('nssapp.urls')),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)