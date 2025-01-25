

from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from accounts.serializers import (SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, 
                                   UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UserSerializer)
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Authentication and User Management Views
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link sent. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)

# Client and Project Management Views
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Customize user creation if needed
        serializer.save()

        return Response({'msg': 'execute Successfully '})



class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the creator
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Ensure 'created_by' is not updated
        instance = serializer.save()
        # Prevent 'created_by' from being overwritten during update
        instance.created_by = self.request.user
        instance.save()
        return Response({'msg': 'execute Successfully '})

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the creator
        serializer.save(created_by=self.request.user)
        return Response({'msg': 'execute Successfully '})

    def perform_update(self, serializer):
        # Ensure 'created_by' is not updated
        instance = serializer.save()
        # Prevent 'created_by' from being overwritten during update
        instance.created_by = self.request.user
        instance.save()
        return Response({'msg': 'execute Successfully '})

    @action(detail=False, methods=['get'], url_path='my-projects')
    def get_user_projects(self, request):
        user = request.user
        projects = user.projects.all()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
        return Response({'msg': 'execute Successfully '})

