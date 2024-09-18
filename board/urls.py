from django.urls import path
from board import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'board'

urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/rate/', views.rate_post, name='rate_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

