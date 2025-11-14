from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.faculty_login, name='faculty_login'),
    path('logout/', views.faculty_logout, name='faculty_logout'),
    path('dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/submissions/', views.view_submissions, name='view_submissions'),
    path('group/<int:group_id>/accept/', views.accept_group, name='accept_group'),
    path('group/<int:group_id>/reject/', views.reject_group, name='reject_group'),
    path('select/<int:group_id>/', views.select_group, name='select_group'),
    path('delete/<int:group_id>/', views.delete_group, name='delete_group'),



]
