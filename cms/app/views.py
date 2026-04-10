from django.shortcuts import render, redirect
from django.db.models import Count
from .models import *

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        User.objects.create(username=username, password=password, role=role)
        return redirect('login')

    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username, password=password).first()

        if user:
            request.session['user'] = user.id
            request.session['role'] = user.role

            if user.role == "teacher":
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')

    return render(request, 'login.html')

def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

def add_course(request):
    if request.method == "POST":
        title = request.POST['title']
        teacher_id = request.session['user']

        Course.objects.create(title=title, teacher_id=teacher_id)
        return redirect('teacher_dashboard')

    return render(request, 'add_course.html')

def teacher_dashboard(request):
    teacher_id = request.session['user']

    courses = Course.objects.filter(teacher_id=teacher_id)

    # Count students per course
    course_data = Course.objects.filter(teacher_id=teacher_id) \
        .annotate(student_count=Count('enrollment'))

    labels = [c.title for c in course_data]
    data = [c.student_count for c in course_data]

    return render(request, 'teacher_dashboard.html', {
        'courses': courses,
        'labels': labels,
        'data': data
    })

def student_dashboard(request):
    user_id = request.session['user']

    courses = Course.objects.all()
    enrollments = Enrollment.objects.filter(student_id=user_id)

    return render(request, 'student_dashboard.html', {
        'courses': courses,
        'enrollments': enrollments
    })

def enroll(request, id):
    user_id = request.session['user']
    Enrollment.objects.create(student_id=user_id, course_id=id)
    return redirect('student_dashboard')

def mark_attendance(request, id):
    student_id = request.session['user']

    Attendance.objects.create(
        student_id=student_id,
        course_id=id
    )

    return redirect('student_dashboard')

def upload_assignment(request):
    if request.method == "POST":
        title = request.POST['title']
        file = request.FILES['file']
        course_id = request.POST['course']

        Assignment.objects.create(
            title=title,
            file=file,
            course_id=course_id
        )

        return redirect('teacher_dashboard')

    courses = Course.objects.filter(teacher_id=request.session['user'])
    return render(request, 'upload_assignment.html', {'courses': courses})

def view_assignments(request, id):
    assignments = Assignment.objects.filter(course_id=id)
    return render(request, 'view_assignments.html', {'assignments': assignments})

def logout(request):
    request.session.flush()
    return redirect('login')

def add_review(request, id):
    if request.method == "POST":
        rating = request.POST['rating']
        comment = request.POST['comment']
        user_id = request.session['user']

        Review.objects.create(
            course_id=id,
            student_id=user_id,
            rating=rating,
            comment=comment
        )

        return redirect('student_dashboard')

    return render(request, 'add_review.html')





