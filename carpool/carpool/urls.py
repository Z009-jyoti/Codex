from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('logPage.urls')),
    path('rider/', include('rider.urls')),
    path('driver/', include('driver.urls')),
    path('', lambda request: redirect('login/')),  # Redirect root to login page
]

