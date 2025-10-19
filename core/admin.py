from django.contrib import admin
from .models import User, College, Branch, Complaint, Feedback, News

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'college_type', 'principal', 'created_at']
    list_filter = ['college_type']
    search_fields = ['name']

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'college', 'created_at']
    list_filter = ['college']
    search_fields = ['name', 'code']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'college', 'branch', 'is_active', 'is_suspended']
    list_filter = ['role', 'college', 'is_active', 'is_suspended']
    search_fields = ['username', 'email', 'roll_number']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'college', 'branch', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'college', 'branch']
    search_fields = ['title', 'description']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'complaint', 'created_at']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'college', 'posted_at']
    list_filter = ['college']
