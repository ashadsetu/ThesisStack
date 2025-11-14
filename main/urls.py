
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),   # <- make sure this line exists
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('supervisor/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('upload/', views.upload_thesis, name='upload_thesis'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
