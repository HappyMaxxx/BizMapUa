from django.contrib import admin
from .models import Region

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'koatuu', 'img')  
    list_filter = ('koatuu', 'value', 'name')
    search_fields = ('name', 'koatuu') 
    ordering = ('name',)