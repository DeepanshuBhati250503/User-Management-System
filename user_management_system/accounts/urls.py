from django.urls import path
from .views import user_list, add_user, edit_user, delete_user, role_list, add_role, edit_role, delete_role 
from .views import home, user_logout, assign_role

urlpatterns = [
    path('', home, name='home'),
    path('logout/', user_logout, name='logout'),
    
    path('users/', user_list, name='user_list'),
    path('users/add/', add_user, name='add_user'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    
    path('users/<int:user_id>/assign-role/', assign_role, name='assign_role'),

    path('roles/', role_list, name='role_list'),
    path('roles/add/', add_role, name='add_role'),
    path('roles/edit/<int:role_id>/', edit_role, name='edit_role'),
    path('roles/delete/<int:role_id>/', delete_role, name='delete_role'),
]