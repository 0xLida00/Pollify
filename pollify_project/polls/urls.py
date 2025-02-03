from django.urls import path
from . import views

urlpatterns = [
    path("", views.PollListView.as_view(), name="poll_list"),
    path("new/", views.PollCreateView.as_view(), name="poll_create"),
    path("<int:pk>/", views.PollDetailView.as_view(), name="poll_detail"),
    path("<int:pk>/vote/", views.vote_poll, name="vote_poll"),
    path("<int:pk>/delete/", views.PollDeleteView.as_view(), name="poll_delete"),
    path("<int:pk>/edit/", views.PollEditView.as_view(), name="poll_edit"),
    path('toggle-follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
]