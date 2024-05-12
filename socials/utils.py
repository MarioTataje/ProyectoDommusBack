from .models import Match
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


model = None


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


def prepare_model():
    url = 'https://raw.githubusercontent.com/MarioTataje/lhs-dataset/main/ckd.csv'
    data = pd.read_csv(url)
    x = data[['user_energy', 'user_mind', 'user_nature', 'user_tactics', 'user_identity']]
    y = data[['ideal_energy', 'ideal_mind', 'ideal_nature', 'ideal_tactics', 'ideal_identity']]

    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)


def predict_ideal_roomate(user):
    personality_profile = user.self_personality.get_personality_profile()
    personality_profile = np.array(personality_profile).reshape(1, -1)
    return personality_profile
    #ideal_profile = model.predict(personality_profile)
    #return ideal_profile.tolist()
