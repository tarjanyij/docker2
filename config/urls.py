from django.contrib import admin
from django.urls import path, include
from dashboard.views import logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include('api.urls')),
	path('', include('dashboard.urls')),
	# explicit logout view (accepts GET) and then include default auth URLs
	path('accounts/logout/', logout_view, name='logout'),
	path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
	# Serve static files from STATIC_ROOT in development/debug mode
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
