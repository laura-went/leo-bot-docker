from django.contrib import admin
from .models import User
from import_export.admin import ImportExportModelAdmin

@admin.register(User)
class ViewAdmin(ImportExportModelAdmin):
    pass
