from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.student_login, name='student_login'),
    path('profile/', views.profile_edit, name='profile_edit'),
    path('logout/', views.student_logout, name='student_logout'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('thesis/upload/', views.upload_thesis, name='upload_thesis'),
    path('feedback/', views.view_feedback, name='view_feedback'),
    path('groups/', views.created_groups, name='created_groups'),

]
