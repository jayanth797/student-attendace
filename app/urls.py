from django.urls import path
from . import views

urlpatterns = [
    path('', views.mark_attendance, name='mark_attendance'),
    path('add-student/', views.add_student, name='add_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('export/', views.export_csv, name='export_csv'),
    path('export/excel/', views.export_excel, name='export_excel'),
]