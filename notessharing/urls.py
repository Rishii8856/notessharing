from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.Index, name='index'),

    # 👉 ONLY ONE notes route (FINAL)
    path('notes/', views.NOTES_DETAILS, name='notes'),

    # बाकी routes
    path('login/', views.LOGIN, name='login'),
    path('dologin/', views.doLogin, name='doLogin'),
    path('logout/', views.doLogout, name='logout'),

    path('', include('nssapp.urls')),  # other app routes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)