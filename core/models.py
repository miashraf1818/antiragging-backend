from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('principal', 'Principal'),
        ('squad', 'Squad'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    college = models.ForeignKey('College', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"


class College(models.Model):
    COLLEGE_TYPE_CHOICES = (
        ('engineering', 'Engineering'),
        ('puc', 'PUC'),
        ('diploma', 'Diploma'),
        ('iti', 'ITI'),
        ('masters', 'Masters'),
    )
    name = models.CharField(max_length=200)
    college_type = models.CharField(max_length=20, choices=COLLEGE_TYPE_CHOICES)
    principal = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_college')
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.college_type})"


class Branch(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.college.name}"

    class Meta:
        verbose_name_plural = "Branches"


class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('solved', 'Solved'),
        ('closed', 'Closed'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='complaints', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='complaints', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, related_name='assigned_complaints', null=True, blank=True,
                                    on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # ✅ ADD THIS FIELD:
    is_anonymous = models.BooleanField(default=False, help_text="If True, student identity is hidden")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.student.username}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='feedbacks')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username}"


class News(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts')
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='news', null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "News"
