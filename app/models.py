from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    class_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()  # True = Present

    def __str__(self):
        return f"{self.student.name} - {self.date}"