from django.urls import path
from . import views

app_name = 'comments'  

urlpatterns = [
    path('add/<int:poll_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/<str:vote_type>/', views.vote_comment, name='vote_comment'),
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]