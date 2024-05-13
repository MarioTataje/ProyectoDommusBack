from django.urls import path

from .views import send_like, send_dislike, get_matches, get_received_likes, get_given_likes,get_profiles, get_ideal_personality, get_ideal_rommates

urlpatterns = [
    path('senders/<int:sender_id>/receivers/<int:receiver_id>/send-like/', send_like, name='send_like'),
    path('senders/<int:sender_id>/receivers/<int:receiver_id>/send-dislike/', send_dislike, name='send_dislike'),
    path('users/<int:user_id>/matches/', get_matches, name='get_matches'),
    path('users/<int:user_id>/received-likes/', get_received_likes, name='get_received_likes'),
    path('users/<int:user_id>/given-likes/', get_given_likes, name='get_given_likes'),
    path('users/<int:user_id>/profiles/', get_profiles, name='get_profiles'),
    path('users/<int:user_id>/ideal-personality/', get_ideal_personality, name='get_ideal_personality'),
    path('users/<int:user_id>/ideal-rommates/', get_ideal_rommates, name='get_ideal_rommates')
]
