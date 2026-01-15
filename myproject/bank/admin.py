from django.contrib import admin
from .models import Register

# Register Branch model
@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','account_num','upi_id','registered_at','profile_picture')       
    search_fields = ('name',)            
