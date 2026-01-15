from django.contrib import admin
from .models import Branch

# Register Branch model
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','city')        # Show ID and name in list
    search_fields = ('name','city')            # Add search box by name
