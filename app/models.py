from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()

    class Meta:
        unique_together = ['student', 'date']  # prevents duplicate attendance

    def __str__(self):
        return f"{self.student.name} - {self.date}"