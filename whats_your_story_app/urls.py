from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name ='index'),
    path('login', views.login, name ='login'),
    path('register', views.register, name ='register'),
    path('profile', views.profile, name ='profile'),
    path('all_stories',views.all_stories, name ='all_stories'),
    path('stories/create', views.create, name = 'create'),
    path('stories/<int:id>/upload', views.upload, name='upload'),
    # Upload Pics is method for uploading_pics, commented out for server maintenance
    path('stories/<int:id>/image_upload', views.image_upload, name='image_upload'),
    path('stories/<int:id>/story', views.story, name ='story'),
    path('stories/<int:id>/edit', views.edit, name ='edit'),
    path('stories/<int:id>/delete', views.delete, name ='delete'),
    path('stories/<int:id>/like_story', views.like_story, name ='like_story'),
    path('stories/<int:id>/unlike_story', views.unlike_story, name ='unlike_story'),
    path('stories/<int:id>/post_comment', views.post_comment, name ='post_comment'),
    path('stories/logout', views.logout, name ='logout'),
    path('delete/image/<int:id>/<int:img_id>', views.image_delete, name="image_delete"),
    path('admin', admin.site.urls)
]



