from .models import Match
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from accounts.models import Personality, User
from datetime import date

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
        exist_like = Match.objects.create(sender_user=sender, receiver_user=receiver, register_date=date.today())
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
                                            flag_match=False, flag_dismatch=True, register_date=date.today())
    return exist_dislike
    

def find_match(sender, receiver):
    try:
        match = Match.objects.get(sender_user__id=sender.id, receiver_user__id=receiver.id)
        return match
    except Match.DoesNotExist:
        return None


def prepare_model():
    global model
    url = 'https://raw.githubusercontent.com/alvaromlua/dommus-dataset/main/dataset.csv'
    data = pd.read_csv(url, delimiter=';')
    x = data[['user_energy', 'user_mind', 'user_nature', 'user_tactics', 'user_identity']]
    y = data[['ideal_energy', 'ideal_mind', 'ideal_nature', 'ideal_tactics', 'ideal_identity']]

    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)


def predict_ideal_personality(user):
    personality = user.self_personality
    if not personality:
        raise ValueError('No tiene personalidad registrada')
    personality_profile = personality.get_personality_profile()
    ideal_profile = model.predict([personality_profile])[0]
    return Personality.get_ideal_personality(ideal_profile)

def predict_ideal_roommates(ideal_personality):
    margin = 0.5
    
    mind_min = ideal_personality.mind - margin
    mind_max = ideal_personality.mind + margin
    energy_min = ideal_personality.energy - margin
    energy_max = ideal_personality.energy + margin
    nature_min = ideal_personality.nature - margin
    nature_max = ideal_personality.nature + margin
    tactics_min = ideal_personality.tactics - margin
    tactics_max = ideal_personality.tactics + margin
    identity_min = ideal_personality.identity - margin
    identity_max = ideal_personality.identity + margin

    
    users = User.objects.filter(
        self_personality__mind__range=(mind_min, mind_max),
        self_personality__energy__range=(energy_min, energy_max),
        self_personality__nature__range=(nature_min, nature_max),
        self_personality__tactics__range=(tactics_min, tactics_max),
        self_personality__identity__range=(identity_min, identity_max)
    )
    return users