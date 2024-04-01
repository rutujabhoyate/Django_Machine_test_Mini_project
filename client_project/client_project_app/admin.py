from django.contrib import admin
from .models import Client, Project

class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'created_at', 'created_by','updated_at')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'client', 'created_at', 'created_by')

admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)




