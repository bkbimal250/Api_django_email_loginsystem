



from django.contrib import admin
from .models import User, Client, Project

# Customizing the User admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

# Customizing the Client admin
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'client_phone', 'address', 'created_by')
    search_fields = ('client_name', 'client_email')
    list_filter = ('client_name',)
    filter_horizontal = ()  # No Many-to-Many field for 'users' in Client model.

# Customizing the Project admin
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_description', 'project_client', 'get_working_users', 'created_by')
    search_fields = ('project_name', 'project_client')
    list_filter = ('project_client', 'project_name')
    filter_horizontal = ('working_users',)  # For Many-to-Many relationships

    # Custom method to display related working_users
    def get_working_users(self, obj):
        return ", ".join([user.email for user in obj.working_users.all()])
    get_working_users.short_description = 'Working Users'  # Set a human-readable name for the column

# Register models with admin site
admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)

