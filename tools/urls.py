from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# admin.site.site_header = "My_Home Admin"
# admin.site.site_title = "My_Home Admin"
# admin.site.index_title = "Welcome To My_Home Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mail_app.urls')),
    path('', include('tooling.urls')),
    path('', include('pdf_app.urls')),
    path('', include('xls_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)