from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('outbox/', views.outbox, name='outbox'),
    path('compose/', views.compose_message, name='compose_message'),
    path('message/<int:message_id>/', views.read_message, name='read_message'),
    path('message/sent/<int:message_id>/', views.message_detail, name='message_detail'),
]