from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve


from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('store.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {
            "document_root": settings.MEDIA_ROOT
        }),
]
