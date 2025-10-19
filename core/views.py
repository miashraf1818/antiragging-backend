from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import *
from .models import User, College, Branch, Complaint, Feedback, News
from django.contrib.auth import get_user_model
from .permissions import IsStudent, IsPrincipal, IsSquad, IsPrincipalOrSquad

# 📧 EMAIL IMPORTS
from core.utils.email_utils import (
    send_complaint_submitted_email,
    send_complaint_status_update_email,
    send_complaint_assigned_email,
    send_welcome_email
)

import logging

logger = logging.getLogger(__name__)
User = get_user_model()


# REST OF YOUR CODE STAYS THE SAME...
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        """Create user and send welcome email"""
        user = serializer.save()

        # 📧 SEND WELCOME EMAIL
        try:
            send_welcome_email(user)
            logger.info(f"✅ Welcome email sent to {user.email}")
        except Exception as e:
            logger.error(f"❌ Failed to send welcome email: {e}")

    def create(self, request, *args, **kwargs):
        """Override to add better error logging"""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            # 🐛 LOG VALIDATION ERRORS
            logger.error(f"❌ User creation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# College & Branch APIs
class CollegeListAPI(generics.ListCreateAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BranchListAPI(generics.ListCreateAPIView):
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        college_id = self.request.query_params.get('college')
        if college_id:
            return Branch.objects.filter(college_id=college_id)
        return Branch.objects.all()


# Complaint APIs
class ComplaintListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = user.role

        if role == 'admin':
            return Complaint.objects.all()
        elif role == 'principal':
            return Complaint.objects.filter(college=user.college)
        elif role == 'squad':
            return Complaint.objects.filter(assigned_to=user)
        else:  # student
            return Complaint.objects.filter(student=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save complaint
            complaint = serializer.save(
                student=request.user,
                college=request.user.college,
                branch=request.user.branch
            )

            # 📧 SEND EMAIL - Complaint Submitted
            try:
                send_complaint_submitted_email(complaint)
                logger.info(f"Complaint submitted email sent for #{complaint.id}")
            except Exception as e:
                logger.error(f"Failed to send complaint email: {e}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplaintDetailAPI(generics.RetrieveUpdateAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        complaint = self.get_object()
        user = request.user

        # Only principal, squad, and admin can update
        if user.role not in ['admin', 'principal', 'squad']:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        # Store old values before update
        old_status = complaint.status
        old_assigned = complaint.assigned_to

        # Perform update
        response = self.partial_update(request, *args, **kwargs)

        # Refresh complaint from DB
        complaint.refresh_from_db()

        # 📧 SEND EMAIL - Status Changed
        if old_status != complaint.status:
            try:
                send_complaint_status_update_email(complaint, old_status)
                logger.info(f"Status update email sent for #{complaint.id}")
            except Exception as e:
                logger.error(f"Failed to send status email: {e}")

        # 📧 SEND EMAIL - Complaint Assigned
        if old_assigned != complaint.assigned_to and complaint.assigned_to:
            try:
                send_complaint_assigned_email(complaint)
                logger.info(f"Assignment email sent for #{complaint.id}")
            except Exception as e:
                logger.error(f"Failed to send assignment email: {e}")

        return response


# User Management (for Principal & Admin)
class StudentListAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.filter(role='student')
        elif user.role == 'principal':
            return User.objects.filter(college=user.college, role='student')
        return User.objects.none()


class StudentDetailAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        if user.role in ['admin', 'principal']:
            return self.partial_update(request, *args, **kwargs)
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)


# Feedback APIs
class FeedbackListCreateAPI(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        complaint_id = self.request.query_params.get('complaint')
        return Feedback.objects.filter(complaint_id=complaint_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# News (Admin creates, everyone views)
class NewsListCreateAPI(generics.ListCreateAPIView):
    queryset = News.objects.all().order_by('-posted_at')
    serializer_class = NewsSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# User ViewSet for Admin
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return User.objects.all()
        elif user.role == 'principal':
            return User.objects.filter(college=user.college)
        elif user.role == 'squad':
            return User.objects.filter(college=user.college)
        else:
            return User.objects.filter(id=user.id)


# Suspend Student
class SuspendStudentAPI(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsPrincipal]

    def update(self, request, *args, **kwargs):
        student = self.get_object()

        if student.college_id != request.user.college_id:
            return Response(
                {'error': 'You can only suspend students from your college'},
                status=status.HTTP_403_FORBIDDEN
            )

        if student.role != 'student':
            return Response(
                {'error': 'You can only suspend students'},
                status=status.HTTP_400_BAD_REQUEST
            )

        student.is_suspended = True
        student.save()

        serializer = self.get_serializer(student)
        return Response(serializer.data)


# Unsuspend Student
class UnsuspendStudentAPI(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsPrincipal]

    def update(self, request, *args, **kwargs):
        student = self.get_object()

        if student.college_id != request.user.college_id:
            return Response(
                {'error': 'You can only unsuspend students from your college'},
                status=status.HTTP_403_FORBIDDEN
            )

        if student.role != 'student':
            return Response(
                {'error': 'You can only unsuspend students'},
                status=status.HTTP_400_BAD_REQUEST
            )

        student.is_suspended = False
        student.save()

        serializer = self.get_serializer(student)
        return Response(serializer.data)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]  # ✅ FIX #1

    def get_queryset(self):
        user = self.request.user

        # ✅ FIX #2: Safety check
        if not user.is_authenticated:
            return Feedback.objects.none()

        logger.info(f"Feedback request by: {user.username} (Role: {user.role})")

        # Admin sees all feedback
        if user.role == 'admin' or user.is_superuser:
            return Feedback.objects.all().order_by('-created_at')

        # Principal sees feedback from their college
        elif user.role == 'principal':
            if not user.college:
                return Feedback.objects.none()
            return Feedback.objects.filter(user__college=user.college).order_by('-created_at')

        # Squad sees feedback from their college
        elif user.role == 'squad':
            if not user.college:
                return Feedback.objects.none()
            return Feedback.objects.filter(user__college=user.college).order_by('-created_at')

        # Student sees only their own feedback
        else:
            return Feedback.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
