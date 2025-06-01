from django.contrib import admin
from django.urls import include, path, re_path

from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static

from django.views.static import serve
from mainapp.views import page_not_found, server_error

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('mainapp.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),]

handler404 = page_not_found
handler500 = server_error