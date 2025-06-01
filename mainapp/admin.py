from django.contrib import admin
from .models import Region, Businesse, Evaluation, BuisnessePhoto

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'koatuu', 'img')  
    list_filter = ('koatuu', 'value', 'name')
    search_fields = ('name', 'koatuu') 
    ordering = ('name',)

@admin.register(Businesse)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'city', 'status')  
    list_filter = ('user', 'region')
    search_fields = ('user', 'name') 

@admin.register(BuisnessePhoto)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('businesse', 'img')  
    search_fields = ('businesse',) 

@admin.register(Evaluation)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'business', 'created_at')  
    list_filter = ('user', 'business', 'rating')
    search_fields = ('user', 'business') 