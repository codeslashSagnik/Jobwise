from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserSignupView, name='register'),
    path('me/', views.currentUser, name='current_user'),
    path('me/update/', views.updateUser, name='update_user'),
    path('me/upload/', views.uploadResume, name='upload_resume'),
]