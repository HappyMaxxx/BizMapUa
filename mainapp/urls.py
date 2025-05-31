from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('', views.index, name='home'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='auth'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('profile/', views.profileview, name='profile'),
    path('map/', views.mapview, name='map'),
    path('region/<int:koatuu>/', views.regionview, name='region')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)