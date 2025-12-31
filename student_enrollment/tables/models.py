from django.db import models

# Create your models here.
class student(models.Model):
    s_fname = models.CharField(max_length=30)
    s_lname = models.CharField(max_length=30)
    s_email = models.EmailField(max_length=150, unique=True)
    s_phone = models.IntegerField(default=0)
    s_dob = models.DateField()
    s_city = models.CharField(max_length=50)
    s_password = models.CharField(max_length=20)
    s_image = models.ImageField(upload_to='media/profilepic')
    s_document = models.FileField(upload_to='media/documents')
    s_bio = models.TextField()

class Course(models.Model):
    c_number = models.CharField(max_length=20, unique=True)
    c_name = models.CharField(max_length=200)
    c_des = models.TextField()
    c_teacher = models.CharField(max_length=100)
    c_credit = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class enrollment(models.Model):
    s_email = models.CharField(max_length=100)
    c_number = models.CharField(max_length=20)
    status = models.CharField(max_length=5,default='p')

class admin(models.Model):
    a_name = models.CharField(max_length=50)
    a_password = models.CharField(max_length=20)


