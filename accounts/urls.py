

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView,
                    SendPasswordResetEmailView, UserPasswordResetView, UserViewSet, ClientViewSet, ProjectViewSet)

# Router for ViewSets
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('clients', ClientViewSet, basename='client')
router.register('projects', ProjectViewSet, basename='project')

urlpatterns = [
    # Authentication and User Management URLs
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    
    # Include the router URLs for the ViewSets
    path('', include(router.urls)),
]
