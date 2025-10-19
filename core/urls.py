from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register(r'feedback', FeedbackViewSet)  # NEW ViewSet

urlpatterns = [
    # Auth
    path('register/', RegisterAPI.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # College & Branch
    path('colleges/', CollegeListAPI.as_view(), name='college_list'),
    path('branches/', BranchListAPI.as_view(), name='branch_list'),

    # Complaints
    path('complaints/', ComplaintListCreateAPI.as_view(), name='complaint_list_create'),
    path('complaints/<int:pk>/', ComplaintDetailAPI.as_view(), name='complaint_detail'),

    # Students Management
    path('students/', StudentListAPI.as_view(), name='student_list'),
    path('students/<int:pk>/', StudentDetailAPI.as_view(), name='student_detail'),
    path('students/<int:pk>/suspend/', SuspendStudentAPI.as_view(), name='student_suspend'),
    path('students/<int:pk>/unsuspend/', UnsuspendStudentAPI.as_view(), name='student_unsuspend'),

    # Feedback - REMOVED OLD ENDPOINT!
    # path('feedback/', FeedbackListCreateAPI.as_view(), name='feedback_list_create'),

    # News
    path('news/', NewsListCreateAPI.as_view(), name='news_list_create'),
]

urlpatterns += router.urls
