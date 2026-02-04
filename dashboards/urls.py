from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # category crud
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    # blog/post crud
    path('posts/', views.posts, name='posts'),
    path('apply_to_write/', views.apply_to_write, name='apply_to_write'),
    path('all_pub_posts/', views.all_pub_posts, name='all_pub_posts'),
    path('posts_review/', views.posts_review, name='posts_review'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('posts/delete/<int:pk>/', views.delete_post, name='delete_post'), 
    # users  crud
    path('users/', views.users, name='users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),
]
