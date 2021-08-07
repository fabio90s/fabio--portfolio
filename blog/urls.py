from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.blogList, name='bloglist'),
    path('create/', views.CreateBlog.as_view(), name='create'),
    path('update/<int:pk>/', views.UpdateBlog.as_view(), name='blogupdate'),
    path('article/<int:pk>/', views.articleView, name='viewarticle'),
    path('add-article', views.addArticle, name='add-article'),
    path('edit-article/<int:pk>/', views.modifyArticle, name='edit-article'),
    path('delete-article/<int:pk>/', views.deleteArticle, name='delete-article'),

]
