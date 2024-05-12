from .models import Match

def verify_like(sender, receiver):
    
    same_like = find_match(sender, receiver)
    if same_like:
        return same_like
    
    exist_like = find_match(receiver, sender)
    
    if exist_like:
        if not (exist_like.is_active or exist_like.flag_dismatch):
            exist_like.flag_match = True
            exist_like.flag_dismatch = False
            exist_like.is_active = True
            exist_like.save()
    else:
        exist_like = Match.objects.create(sender_user=sender, receiver_user=receiver)
    return exist_like
    

def verify_dislike(sender, receiver):
    
    same_dislike = find_match(sender, receiver)
    if same_dislike:
        return same_dislike
    
    exist_dislike = find_match(receiver, sender)
    
    if exist_dislike:
        if not exist_dislike.flag_dismatch:
            exist_dislike.flag_match = False
            exist_dislike.flag_dismatch = True
            exist_dislike.save()
    else:
        exist_dislike = Match.objects.create(sender_user=sender, receiver_user=receiver, 
                                            flag_match=False, flag_dismatch=True)
    return exist_dislike
    

def find_match(sender, receiver):
    try:
        match = Match.objects.get(sender_user__id=sender.id, receiver_user__id=receiver.id)
        return match
    except Match.DoesNotExist:
        return None
