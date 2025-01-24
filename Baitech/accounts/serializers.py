from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import User, Client, Project
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.utils import Util  # Adjust the import based on your project structure

# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

# User Login Serializer
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

# User Change Password Serializer
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password don't match")
        user.set_password(password)
        user.save()
        return attrs

# Send Password Reset Email Serializer
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            print("token:", token)
            link = f'http://localhost:3000/api/user/reset/{uid}/{token}'
            body = f'Click the following link to reset your password: {link}'
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email,
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')

# User Password Reset Serializer
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password don't match")
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not valid or has expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError('Token is not valid or has expired')

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

# Client Serializer

# Client Serializer
class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['created_by']  # Prevent users from manually setting it

    def get_created_by(self, obj):
        if obj.created_by:
            full_name = f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
            return full_name if full_name else obj.created_by.email
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['created_by'] = request.user  # Automatically set created_by to the logged-in user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('created_by', None)  # Ensure created_by cannot be modified
        return super().update(instance, validated_data)


# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    working_users = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), many=True)  # Correct setup for Many-to-Many
    project_client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())  # Foreign key to Client

    def get_created_by(self, obj):
        if obj.created_by:
            full_name = f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
            return full_name if full_name else obj.created_by.email
        return None

    def get_working_users(self, obj):
        return [user.email for user in obj.working_users.all()]  # List of user emails (replace with user.username if needed)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_by']  # Prevent users from manually setting 'created_by'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['created_by'] = request.user  # Automatically set created_by to the logged-in user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('created_by', None)  # Ensure created_by cannot be modified
        return super().update(instance, validated_data)

