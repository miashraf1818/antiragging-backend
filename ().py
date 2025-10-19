# coding: utf-8
from django.contrib.auth import get_user_model
User = get_user_model()

student = User.objects.get(username='student1')
student.set_password('student123')
student.is_active = True
student.is_suspended = False
student.save()
print(f"Student1 password reset. Active: {student.is_active}, Suspended: {student.is_suspended}")
\ password reset. Active: {student.is_active}, Suspended: {student.is_suspended}")
