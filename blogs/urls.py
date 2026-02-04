from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
     # Search endpoint
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('search/', views.search, name='search'),
    path('blogs/<slug:slug>/', views.blogs, name='blogs'),
    
]