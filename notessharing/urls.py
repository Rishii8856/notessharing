from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.Index, name='index'),

    path('login/', views.LOGIN, name='login'),
    path('dologin/', views.doLogin, name='doLogin'),
    path('logout/', views.doLogout, name='logout'),

    # 🔥 IMPORTANT FIX
    path('notes/', views.NOTES_DETAILS, name='notes'),

    path('', include('nssapp.urls')),
]