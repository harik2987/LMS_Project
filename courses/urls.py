from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('upload/', views.upload_content, name='upload_content'),
    path('scorm/play/<int:id>/', views.play_scorm, name='play_scorm'),
    path('scorm/play/view/<int:course_id>/', views.scorm_playback, name='scorm_playback'),
    path('scorm/runtime/update/<int:course_id>/', views.scorm_runtime_update, name='scorm_runtime_update'),
]
