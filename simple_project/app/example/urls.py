from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def home_view(request):
    return HttpResponse('Добро пожаловать на главную страницу!')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('movies.api.urls')),
    path('', home_view),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
