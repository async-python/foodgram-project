from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += staticfiles_urlpatterns()

handler404 = 'recipes.views.page_not_found'
handler500 = 'recipes.views.server_error'
