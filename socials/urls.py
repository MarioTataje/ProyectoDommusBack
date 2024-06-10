from django.urls import path

from .views import send_like, send_dislike, get_matches, delete_match, get_received_likes, get_given_likes,get_profiles, get_ideal_personality, get_ideal_rommates, report_user, get_reports_by_reporting, get_reports_by_reported  

urlpatterns = [
    path('senders/<int:sender_id>/receivers/<int:receiver_id>/send-like/', send_like, name='send_like'),
    path('senders/<int:sender_id>/receivers/<int:receiver_id>/send-dislike/', send_dislike, name='send_dislike'),
    path('users/<int:user_id>/matches/', get_matches, name='get_matches'),
    path('matches/<int:match_id>/', delete_match, name='delete_match'),
    path('users/<int:user_id>/received-likes/', get_received_likes, name='get_received_likes'),
    path('users/<int:user_id>/given-likes/', get_given_likes, name='get_given_likes'),
    path('users/<int:user_id>/profiles/', get_profiles, name='get_profiles'),
    path('users/<int:user_id>/ideal-personality/', get_ideal_personality, name='get_ideal_personality'),
    path('users/<int:user_id>/ideal-rommates/', get_ideal_rommates, name='get_ideal_rommates'),
    path('reporting/<int:reporting_id>/reported/<int:reported_id>/reports/', report_user, name='report_user'),
    path('reporting/<int:reporting_id>/reports/', get_reports_by_reporting, name='get_reports_by_reporting'),
    path('reported/<int:reported_id>/reports/', get_reports_by_reported, name='get_reports_by_reported')
]
