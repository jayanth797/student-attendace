from django.shortcuts import render, redirect
from .models import Student, Attendance
from datetime import date
from django.db.models import Count, Q
import json
import csv
from django.http import HttpResponse


def mark_attendance(request):
    students = Student.objects.all()
    today = request.GET.get('date') or str(date.today())

    if request.method == "POST":
        print("POST DATA:", request.POST)
        selected_date = request.POST.get("date") or str(date.today())
        action = request.POST.get("action", "save")

        if action == "reset":
            Attendance.objects.filter(date=selected_date).delete()
            messages.success(request, f"Attendance for {selected_date} has been reset.")
            return redirect('/')

        if Attendance.objects.filter(date=selected_date).exists():
            messages.warning(request, "Attendance already marked for this date.")
            return redirect('/')

        for student in students:
            status = str(student.id) in request.POST

            Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={'status': status}
            )
            
        messages.success(request, f"Attendance for {selected_date} saved successfully!")
        return redirect('/')

    return render(request, 'students.html', {
        'students': students,
        'today': today
    })


def attendance_report(request):
    students = Student.objects.all()

    report = []
    names = []
    percentages = []

    for student in students:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status=True).count()

        percentage = int((present / total) * 100) if total > 0 else 0

        report.append({
            'name': student.name,
            'total': total,
            'present': present,
            'percentage': percentage
        })

        names.append(student.name)
        percentages.append(percentage)

    return render(request, 'report.html', {
        'report': report,
        'names': json.dumps(names),
        'percentages': json.dumps(percentages)
    })


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Total Days', 'Present Days', 'Percentage'])

    students = Student.objects.all()

    for student in students:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status=True).count()
        percentage = int((present / total) * 100) if total > 0 else 0

        writer.writerow([student.name, total, present, percentage])

    return response
from django.contrib import messages

def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if name:
            Student.objects.create(name=name)
            messages.success(request, f"Student '{name}' added successfully!")
        else:
            messages.error(request, "Student name cannot be empty.")

    return redirect('mark_attendance')