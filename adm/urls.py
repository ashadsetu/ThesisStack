from django.urls import path
from . import views

app_name = "adm"

urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("users/", views.manage_users, name="manage_users"),
    path("students/", views.student_list, name="student_list"),
    path("faculty/", views.faculty_list, name="faculty_list"),
    path("user/<int:user_id>/", views.user_detail, name="user_detail"),
    path("user/<int:user_id>/edit/", views.edit_user, name="edit_user"),
    path("user/<int:user_id>/delete/", views.delete_user, name="delete_user"),
]
