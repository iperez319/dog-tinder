from models import UserProfile
from models import Dog

def save_profile(email, name, city, state):
    p = get_user_profile(email)
    if p:
        p.name = name
        p.city = city
        p.state = state
    else:
        p = UserProfile(name=name, email=email, city=city, state=state)
    p.put()
def get_user_profile(email):
    p = UserProfile.query(UserProfile.email == email)
    results = p.fetch(1)
    for profile in results:
        return profile
    return None
def create_dog(email, name, breed, gender, age, size, social, active, friendly, profilePic):
    p = get_user_profile(email)
    newDog = Dog(name=name, breed=breed, gender=gender, socialLevel=social, activityLevel=active, friendlyLevel=friendly, size=size, ownerName=p.name, profilePic=profilePic)
    newKey = newDog.put()
    p.dogs.append(newKey)
    p.put()
