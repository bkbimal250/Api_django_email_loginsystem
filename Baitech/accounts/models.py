


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)  # Normalize the email address
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Set the password properly
        user.save(using=self._db)  # Save the user to the database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True) # user active
    is_staff = models.BooleanField(default=False) #this user cannot update and delete.
    is_admin = models.BooleanField(default=False)  # This field is typically redundant with `is_staff`
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Email will be the unique identifier for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Fields required for creating a user

    def __str__(self):
        return self.email  # Return email as string representation of the user

# Client Model
class Client(models.Model):
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField(unique=True)
    client_phone = models.CharField(max_length=15, blank=True)  # Optional phone number
    address = models.TextField(blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional foreign key to User
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name

# Project Model
class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField(blank=False)
    project_client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE, null=True, blank=True)
      # Foreign key to Client
    working_users = models.ManyToManyField(get_user_model(), related_name='projects')  # Many-to-Many relationship with User
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional foreign key to User
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name
