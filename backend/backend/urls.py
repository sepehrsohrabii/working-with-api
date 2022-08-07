from django.contrib import admin
from django.urls import path, include


app_name = 'apihandler'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apihandler.urls')),
    path('accounts/', include('accounts.urls')),
    path("panel/", include("panel.urls")),
]
