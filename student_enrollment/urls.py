"""
URL configuration for student_enrollment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tables import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin-django/', admin.site.urls),
    path('register/', views.stu_reg, name='registration'),
    path('success/', views.success, name='success'),
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('enroll-courses/', views.courses, name='course'),
    path('logout/', views.logout, name='logout'),
    path('document/', views.document, name='document'),
    path('enroll/', views.enroll_course, name='enroll'),
    path('admin-login/', views.admin_login, name='admin_login'),
    # path('admin/', views.admin_page, name='admin'),
    path('admin/', views.admin_options, name='admin'),
    path('students/', views.st_admin, name='st-admin'),
    path('students/update/<int:student_id>/', views.update_student, name='st-update'),
    path('students/delete/<int:student_id>/', views.delete_student, name='st-delete'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('enrollments/requests/', views.enrollment_requests, name='enrollment_requests'),
    path('enrollments/update/<int:enrollment_id>/', views.update_enrollment, name='update_enrollment'),
    path('accepted/', views.accepted_course, name='accepted'),
    path('rejected/', views.rejected_course, name='rejected'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # path('', RedirectView.as_view(url='/login/')),  # Redirect root to login
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
