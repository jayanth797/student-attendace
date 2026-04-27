from django.urls import path
from . import views

urlpatterns = [
    path('', views.mark_attendance, name='mark_attendance'),
    path('add-student/', views.add_student, name='add_student'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('export/', views.export_csv, name='export_csv'),
]