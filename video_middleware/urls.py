from django.urls import path, include
from . import views
from .views import VideoStream

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('upload_file/',views.upload_file,name='upload_file'),
    path('view_video/<int:video_id>/',VideoStream.as_view(),name='view_video'),
]
