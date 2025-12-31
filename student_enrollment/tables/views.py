from django.shortcuts import render, redirect, get_object_or_404
from .models import student, admin, enrollment, Course
from django.http import HttpResponse 
from django.contrib import messages
import os



def stu_reg(req):
    if req.method == 'POST':
        st_fname = req.POST['s_fname']
        st_lname = req.POST['s_lname']
        st_email = req.POST['s_email']
        st_phone = req.POST['s_phone']
        st_dob = req.POST['s_dob']
        st_city = req.POST['s_city']
        st_password = req.POST['s_password']
        st_bio = req.POST['s_bio']
        
        # Handle file uploads using req.FILES instead of req.POST
        st_image = req.FILES.get('s_image')
        st_document = req.FILES.get('s_document')
        
        # Create student with files
        asign_to_student = student(
            s_fname=st_fname,
            s_lname=st_lname,
            s_email=st_email,
            s_phone=st_phone,
            s_dob=st_dob,
            s_city=st_city,
            s_password=st_password,
            s_image=st_image,
            s_document=st_document,
            s_bio=st_bio
        )
        asign_to_student.save()
        return render(req, 'success.html')
    return render(req, 'student_register.html')

def success(req):
    return render(req, 'success.html')

def login(req):
    req.session.flush()
    if req.method == 'POST':
        st_email = req.POST['username']
        st_password = req.POST['password']
        user = student.objects.get(s_email=st_email, s_password=st_password)
        # Store user ID in session
        req.session['user_id'] = user.id
        if user:
            return redirect('dashboard')
        else:
            return HttpResponse('the user does not exist')
    return render(req, 'student_login.html')


def dashboard(req):
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        user_id = req.session.get('user_id')
        user = student.objects.get(id=user_id)
        enrollments = enrollment.objects.filter(s_email = user.s_email)
        data = []
        for i in enrollments:
            course = Course.objects.get(c_number = i.c_number)
            data.append({
                'course':course
            })
        return render(req, 'dashboard.html',{'user':user , 'enrolled_courses':data})

def courses(req):
    if 'user_id' not in req.session:
        return redirect('login')
    else:
        all_courses = Course.objects.all()
        return render(req, 'course_enrollment.html', {'course':all_courses})

def logout(req):
    req.session.flush()
    return render(req, 'student_login.html')


def document(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login first")
        return redirect('login')
    user_id = request.session['user_id']
    try:
        current_student = student.objects.get(id=user_id)
    except student.DoesNotExist:
        messages.error(request, "Student not found")
        return redirect('login')

    # Assuming s_document is a FileField for one document
    # If you have multiple documents stored differently, please clarify

    documents = []
    if current_student.s_document:
        documents.append({
            'url': current_student.s_document.url,
            'name': os.path.basename(current_student.s_document.name)
        })

    return render(request, 'documents.html', {
        'user': current_student,
        'documents': documents
    })

def enroll_course(request):
    # Get email and course number from request
    user_id = request.session.get('user_id')
    user = student.objects.get(id=user_id)
    courses = Course.objects.all()
    if request.method == 'POST':
        course = request.POST['c_number']
        enroll = enrollment(s_email = user.s_email , c_number = course)
        enroll.save()
        return redirect('enroll')
    return render(request, 'enroll.html', {'user':user, 'courses':courses})

def admin_login(req):
    req.session.flush()
    if req.method == 'POST':
        a_name = req.POST['username']
        a_password = req.POST['password']
        a_check = admin.objects.get(a_name = a_name, a_password = a_password)
        req.session['user_id'] = a_check.pk
        if a_check:
            return redirect('admin')
        else:
            return HttpResponse("You are not an admin")
    return render(req, 'admin_login.html')

def admin_options(req):
    if 'user_id' not in req.session:
        return redirect('admin_login')
    else:
        stu_table = student.objects.count()
        cor_table = Course.objects.count()
        enroll = enrollment.objects.count()
        return render(req, 'admin_options.html',{'student':stu_table, 'course':cor_table, 'enroll':enroll})

def st_admin(req):
    if 'user_id' not in req.session:
        return redirect('admin_login')
    else:
        stu_table = student.objects.all()
        return render(req, 'admin_student.html', {'student':stu_table})


def update_student(request, student_id):
  if 'user_id' not in request.session:
    return redirect('login')
  else:
    students = get_object_or_404(student, id=student_id)
    email_error = None
    if request.method == 'POST':
        try:
            # Check if email is being changed to one that already exists
            new_email = request.POST['s_email']
            if new_email != student.s_email and student.objects.filter(s_email=new_email).exists():
                email_error = "This email is already in use by another student."
            else:
                students.s_fname = request.POST['s_fname']
                students.s_lname = request.POST['s_lname']
                students.s_email = new_email
                students.s_phone = request.POST['s_phone']
                students.s_city = request.POST['s_city']
                students.save()
                messages.success(request, 'Student updated successfully!')
                return redirect('st-admin')
                
        except Exception as e:
            messages.error(request, f'Error updating student: {str(e)}')
    
    return render(request, 'admin_update.html', {
        'student': student,
        'email_error': email_error
    })

def delete_student(request, student_id):
  if 'user_id' not in request.session:
    return redirect('login')
  else:
    students = get_object_or_404(student, id=student_id)
    if request.method == 'POST':
        try:
            students.delete()
            messages.success(request, 'Student deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting student: {str(e)}')
        return redirect('st-admin')
    
    # If not POST, show confirmation (handled by JavaScript)
    return redirect('st-admin')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'admin_course.html', {'courses': courses})

def add_course(request):
  if 'user_id' not in request.session:
    return redirect('login')
  else:
    if request.method == 'POST':
        try:
            Course.objects.create(
                c_number=request.POST['c_number'],
                c_name=request.POST['c_name'],
                c_teacher=request.POST['c_teacher'],
                c_credit=request.POST['c_credit'],
                c_des=request.POST.get('c_des')
            )
            messages.success(request, 'Course added successfully!')
            return redirect('course_list')
        except Exception as e:
            messages.error(request, f'Error adding course: {str(e)}')
    return redirect('course_list')

def delete_course(request, course_id):
  if 'user_id' not in request.session:
    return redirect('login')
  else:
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        try:
            course.delete()
            messages.success(request, 'Course deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting course: {str(e)}')
    return redirect('course_list')

def enrollment_requests(request):
  if 'user_id' not in request.session:
    return redirect('login')
  else:
    enrollments = enrollment.objects.filter(status='p')  # pending enrollments
    data = []
    for enr in enrollments:
        try:
            student_obj = student.objects.get(s_email=enr.s_email)
            course_obj = Course.objects.get(c_number = enr.c_number)

            data.append({
                'student': student_obj,
                'course': course_obj,
                'enrollment': enr
            })
        except (student.DoesNotExist, Course.DoesNotExist):
            continue  # skip if linked student or course not found

    return render(request, 'admin_enrollment.html', {'data': data})

def update_enrollment(request, enrollment_id):
 if 'user_id' not in request.session:
    return redirect('login')
 else:
    if request.method == 'POST':
        enrollments = get_object_or_404(enrollment, id=enrollment_id)
        try:
            new_status = request.POST.get('status')
            if new_status in ['A', 'R']:  # Only allow Accept or Reject
                enrollments.status = new_status
                enrollments.save()
                
                status_display = "accepted" if new_status == 'A' else "rejected"
                messages.success(request, f'Enrollment {status_display} successfully!')
            else:
                messages.error(request, 'Invalid status update')
        except Exception as e:
            messages.error(request, f'Error updating enrollment: {str(e)}')
    return redirect('enrollment_requests')

def accepted_course(req):
        if 'user_id' not in req.session:
            return redirect('login')
        else:
            user_id = req.session.get('user_id')
            user = student.objects.get(id = user_id)
            enrollments = enrollment.objects.filter(status='A', s_email = user.s_email)
            data = []
            for i in enrollments:
                course = Course.objects.get(c_number = i.c_number)
                data.append({
                    'course':course
                    })
            return render(req, 'Enrolled_course.html', {'enrolled_courses': data, 'user':user})

def rejected_course(req):
        if 'user_id' not in req.session:
            return redirect('login')
        else:
            user_id = req.session.get('user_id')
            user = student.objects.get(id = user_id)
            enrollments = enrollment.objects.filter(status='R', s_email = user.s_email)
            data = []
            for i in enrollments:
                course = Course.objects.get(c_number = i.c_number)
                data.append({
                    'course':course
                    })
            return render(req, 'rejected_courses.html', {'enrolled_courses': data, 'user':user})