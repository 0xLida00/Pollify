from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:poll_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/<str:vote_type>/', views.vote_comment, name='vote_comment'),
]