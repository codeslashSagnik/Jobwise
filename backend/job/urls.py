from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.getallJobs, name='jobs'),
    path('jobs/create/', views.createjob, name='create_job'),
    path('jobs/<str:pk>/', views.getJobById, name='job'),
    path('jobs/<str:pk>/update', views.update_job, name='update_job'),
    path('jobs/<str:pk>/delete', views.deleteJob, name='delete_job'),
    path('stats/<str:topic>/', views.getTopicStats, name='get_topic_stats')
]