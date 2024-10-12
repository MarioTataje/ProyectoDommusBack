from .models import Match
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from accounts.models import Personality, User
from datetime import date, datetime
from django.db.models import F, ExpressionWrapper, fields


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
    attributes = ['mind', 'energy', 'nature', 'tactics']
    filters = {
        f'self_personality__{attr}__range': (
            getattr(ideal_personality, attr) - margin,
            getattr(ideal_personality, attr) + margin
        )
        for attr in attributes
    }

    users = User.objects.filter(**filters)

    for user in users:
        user.compatibility = calculate_compatibility(user.self_personality, ideal_personality)
    
    return users


def calculate_compatibility(user_personality, ideal_personality):
    attributes = ['mind', 'energy', 'nature', 'tactics']
    
    total_diff = sum(
        abs(float(getattr(user_personality, attr)) - float(getattr(ideal_personality, attr)))
        for attr in attributes
    )
    max_diff = len(attributes)    
    compatibility = (1 - (total_diff / max_diff)) * 100
        
    return compatibility

def filtrar_ideal_roommates(ideal_roommates, filters):
    sex = filters.get('sex', None)
    age_min = filters.get('age_min', None)
    age_max = filters.get('age_max', None)
    university_id = filters.get('university_id', None)

    if sex is not None:
        ideal_roommates = ideal_roommates.filter(genre=sex)

    today = datetime.today().date()
    age_expression = ExpressionWrapper(
        today.year - F('birth_date__year'),
        output_field=fields.IntegerField()
    )

    if age_min is not None:
        ideal_roommates = ideal_roommates.annotate(age=age_expression).filter(age__gte=age_min)
        print(list(ideal_roommates))

    if age_max is not None:
        ideal_roommates = ideal_roommates.annotate(age=age_expression).filter(age__lte=age_max)

    if university_id is not None:
        ideal_roommates = ideal_roommates.filter(university__id=university_id)

    return ideal_roommates
