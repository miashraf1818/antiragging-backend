from rest_framework import serializers
from .models import User, College, Branch, Complaint, Feedback, News
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
import re

User = get_user_model()


# ============= SMART LOGIN: EMAIL/PHONE/USERNAME =============
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        self.fields['identifier'] = serializers.CharField(
            required=True,
            help_text="Email, Phone Number, or Username"
        )

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        if not identifier:
            raise serializers.ValidationError({
                'identifier': 'This field is required'
            })

        user = None

        # Try EMAIL first (most students will use this)
        if '@' in identifier:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                pass

        # Try PHONE (digits only, students can use this too)
        if not user and identifier.replace('+', '').isdigit():
            try:
                user = User.objects.get(phone=identifier)
            except User.DoesNotExist:
                pass

        # Try USERNAME (fallback for admin/principal/squad)
        if not user:
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError({
                'detail': 'No user found with this email, phone, or username'
            })

        # Check password
        if not user.check_password(password):
            raise serializers.ValidationError({
                'detail': 'Incorrect password'
            })

        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError({
                'detail': 'User account is disabled'
            })

        # Check if suspended
        if hasattr(user, 'is_suspended') and user.is_suspended:
            raise serializers.ValidationError({
                'detail': 'Your account has been suspended. Contact administrator.'
            })

        # Generate tokens
        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'college': user.college.id if user.college else None,
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['college_id'] = user.college.id if user.college else None
        return token


# ============= REST OF THE SERIALIZERS =============
class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)

    class Meta:
        model = Branch
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'college', 'college_name',
                  'branch', 'branch_name', 'roll_number', 'is_active', 'is_suspended']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=False)  # ✅ Optional
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True, max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'phone', 'role', 'college', 'branch', 'roll_number']  # ✅ 'role' is here
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken")
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers, and underscores")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered")
        return value

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already registered")
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        # Optional: Add more password strength checks
        return value

    def validate(self, data):
        """Check if passwords match (only if confirm_password is provided)"""
        # ✅ SAFE CHECK
        if 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError({
                    'confirm_password': 'Passwords do not match'
                })
        return data

    def create(self, validated_data):
        # Remove confirm_password before creating user
        validated_data.pop('confirm_password', None)  # ✅ SAFE REMOVAL

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            college=validated_data.get('college'),
            branch=validated_data.get('branch'),
            roll_number=validated_data.get('roll_number'),
            role=validated_data.get('role', 'student')  # ✅ CORRECT - Gets role from data or defaults to 'student'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ComplaintSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    college_name = serializers.CharField(source='college.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    is_anonymous = serializers.BooleanField(default=False)

    class Meta:
        model = Complaint
        fields = [
            'id',
            'student',
            'college',
            'college_name',
            'branch',
            'branch_name',
            'title',
            'description',
            'status',
            'assigned_to',
            'assigned_to_detail',
            'is_anonymous',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['student', 'college', 'branch', 'created_at', 'updated_at']


class FeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    complaint_title = serializers.CharField(source='complaint.title', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'user_name', 'complaint', 'complaint_title', 'message', 'created_at']
        read_only_fields = ['user', 'created_at']


class NewsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['created_by', 'posted_at']
