from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('', views.index, name='home'),
    path('adminpanel/', views.adminpanelview, name='adminpanel'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='auth'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('profile/', views.profileview, name='profile'),
    path('map/', views.mapview, name='map'),
    path('regions/<str:koatuu>/', views.regionview, name='region'),
    path('create_business', views.create_business, name='create_business'),
    # API
    path('api/check_username/', views.check_username, name='check_username'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)