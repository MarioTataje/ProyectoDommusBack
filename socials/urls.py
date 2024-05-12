from django.urls import path

from .views import send_like, send_dislike

urlpatterns = [
    path('senders/<int:sender_id>/receivers/<int:receiver_id>/send-like/', send_like, name='send_like'),
    path('senders/<int:sender_id>/receivers/<int:receiver_id>/send-dislike/', send_dislike, name='send_dislike')
]
