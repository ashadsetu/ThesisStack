from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def global_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')

urlpatterns = [
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('faculty/', include('faculty.urls')),
    path('adm/', include(('adm.urls', 'adm'), namespace='adm')),
    path('profile/', include(('profiles.urls', 'profiles'), namespace='profiles')),
    path('logout/', global_logout, name='global_logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
