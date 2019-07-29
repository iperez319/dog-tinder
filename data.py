from models import UserProfile
from models import Dog
from google.appengine.ext import ndb
from random import choice

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
    newDog = Dog(name=name, breed=breed, age=age, gender=gender, socialLevel=social, activityLevel=active, friendlyLevel=friendly, size=size, ownerEmail = email, profilePic=profilePic)
    newKey = newDog.put()
    p.dogs.append(newKey)
    p.put()
def get_dog_by_id(ids):
    dogs = Dog.query(Dog.key == ids).fetch(1)
    print(dog)
    for dog in dogs:
        return dog
    return None
def get_local_dogs(email, city, state):
    results = []
    p = UserProfile.query(UserProfile.city == city, UserProfile.state == state, UserProfile.email != email).fetch()
    for profile in p:
        for dog in profile.dogs:
            results.append(dog.get())
    return results
def breed_match(breed1, breed2):
    if breed1 == "Labrador Retriever" or breed2 == "Labrador Retriever" or breed1 == "Beagle" or breed2 == "Beagle":
        return True
    elif breed1 == "Mix" and breed2 == "Mix":
        return True
    dic = {"German Shepherd": ["Labrador", "Golden Retriever", "Border Collie"], "Bulldog": ["Mastiff", "Boxer", "Doberman"], "French Bulldog": ["Boxer", "Greyhound", "Labrador"], "Yorkshire Terrier": ["Border Collie", "Mastiff", "Great Dane"], "Poodle": ["Shi Tzu", "Pekingese", "Pug"], \
    "Rottweiler": ["Sheltie", "Siberian Husky", "Border Collie"], "Boxer": ["Labrador", "Golden Retriever", "Pointer"], "Siberian Husky": ["Alaskan Malamute", "Great Dane", "Malinois"], "Dachshund": ["Labrador", "Maltese", "Pug"], "Great Dane": ["Golden Retriever", "Pointer", "German Shepherd"]}
    if breed1 in dic:
        if breed2 in dic[breed1]:
            return True
    elif breed2 in dic:
        if bree1 in dic[breed2]:
            return True
    else:
        if breed1 == breed2:
            return True
        return False
def age_match(age1, age2):
    diff = abs(int(age1) - int(age2))
    return (diff + 1) * 5
def active_match(active1, active2):
    diff = abs(int(active1) - int(active2))
    return (diff + 1) * 2.5
def gender_match(gender1, gender2):
    if gender1 == gender2:
        return True
    return False
def social_match(social1, social2):
    if social1 == "Shy" and social2 == "Shy":
        return False
    return True
def size_match(size1, size2):
    if size1 == size2:
        return True
    return False
def score_dog(originalDog, dog):
    score = 100
    score -= (not breed_match(originalDog.breed, dog.breed)) * 20
    score -= age_match(originalDog.age, dog.age)
    score -= active_match(originalDog.activityLevel, dog.activityLevel)
    score -= (not gender_match(originalDog.gender, dog.gender)) * 20
    score -= (not social_match(originalDog.socialLevel, dog.socialLevel)) * 10
    score -= (not size_match(originalDog.size, dog.size)) * 20
    return score
def populate_dogs():
    name = ["Fido", "Dashi", "Ian", "Jorge", "Martin", "Igor", "Alina", "Miraf", "Cedes", "Karly"]
    breed = ["German Shepherd", "French Bulldog", "Maltese", "Great Dane", "Shi Tzu", "Pug", "Greyhound"]
    gender = ["Male", "Female"]
    age = ["1", "2", "3", "4"]
    size = ["Toy", "Small", "Medium", "Large", "Extra Large"]
    socialLevel = ["Shy", "Social"]
    activityLevel = ["1", "2", "3", "4"]
    ownerEmail = "testomondongo@example.com"
    dgs = []
    for i in range(25):
        dog = Dog(name=choice(name), breed=choice(breed), gender=choice(gender), age=choice(age), size=choice(size), socialLevel=choice(socialLevel),activityLevel=choice(activityLevel), ownerEmail=ownerEmail)
        dgs.append(dog.put())
    up = UserProfile(name="Testo Mondongo", email=ownerEmail, dogs=dgs, city="San Juan", state="Puerto Rico")
    up.put()
