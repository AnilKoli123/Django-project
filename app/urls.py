from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('add-course/', views.add_course, name='add_course'),
    path('enroll/<int:id>/', views.enroll, name='enroll'),
    path('attendance/<int:id>/', views.mark_attendance, name='attendance'),
    path('upload-assignment/', views.upload_assignment, name='upload_assignment'),
    path('assignments/<int:id>/', views.view_assignments, name='view_assignments'),
    path('logout/', views.logout, name='logout'),
    path('review/<int:id>/', views.add_review, name='add_review'),
]