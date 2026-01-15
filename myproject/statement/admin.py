from django.contrib import admin
from .models import Statement



@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('user','bal','transaction_type','date')
