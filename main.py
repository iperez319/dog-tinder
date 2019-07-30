import os
import data
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from models import Dog

def render_template(handler, file_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/', file_name)
    handler.response.out.write(template.render(path, template_values))
def get_user_email():
    user = users.get_current_user()
    if user:
        return user.email()
    else:
        return None
def get_template_parameters():
    values = {}
    if get_user_email():
        values['logout_url'] = users.create_logout_url('/')
    else:
        values['login_url'] = users.create_login_url('/')
    return values

class MainHandler(webapp2.RequestHandler):
    def get(self):

        values = get_template_parameters()
        if not get_user_email():
            profile = data.get_user_profile(get_user_email())
            if profile:
                values['name'] = profile.name
        render_template(self, 'mainpage.html', values)
class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_template_parameters()
            profile = data.get_user_profile(get_user_email())
            if profile:
                values["name"] = profile.name
                values["email"] = get_user_email()
                values["city"] = profile.city
                values["state"] = profile.state
            render_template(self, 'profile-edit.html', values)
class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            name = self.request.get('name')
            city = self.request.get('city')
            state = self.request.get('state')
            print(city)
            if len(name) < 2:
                error_text += 'Your name must be at least 2 characters.\n'
            if len(name) > 30:
                error_text += 'Your name cannot be more than 30 characters.\n'
            # if len(dogName) < 2:
            #     error_text += "Your dog's name must be at least 2 characters.\n"
            # if len(description) > 4000:
            #     error_text += "Your dog's description is too long; 4000 characters or less.\n"
            # for word in description.split():
            #     if len(word) > 50:
            #         error_text += 'Make each word in your description no longer than 50 characters.\n'
            #         break

            values = get_template_parameters()
            values['name'] = name
            values['email'] = get_user_email()
            values['city'] = city
            values['state'] = state

            if error_text:
                values['errormsg'] = error_text
            else:
                data.save_profile(email, name, city, state)
                values['successmsg'] = 'Successfully saved!'
            self.redirect('/profile-view')
            #render_template(self, 'profile-edit.html', values)

class ProfileViewHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_template_parameters()
            profile = data.get_user_profile(get_user_email())
            if profile:
                values['name'] = profile.name
                values['city'] = profile.city
                values['state'] = profile.state
                dogs = []
                for dog in profile.dogs:
                    currDog = dog.get()
                    currDog.keyUrl = currDog.key.urlsafe()
                    print(currDog.keyUrl)
                    dogs.append(currDog)
                values['dogs'] = dogs
                #data.populate_dogs()
            render_template(self, 'profile-view.html', values)
class AddDogHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_template_parameters()
            profile = data.get_user_profile(get_user_email())
            if not profile:
                self.redirect('/profile-edit')
            render_template(self, 'add-dog.html', values)
    def post(self):
        if not get_user_email():
            self.redirect('/')
        else:
            name = self.request.get('name')
            breed = self.request.get('breed')
            gender = self.request.get('gender')
            age = self.request.get('age')
            size = self.request.get('size')
            social = self.request.get('social')
            active = self.request.get('active')
            friendly = self.request.get('friendly')
            profilePic = self.request.get('profilePic')
        data.create_dog(get_user_email(), name, breed, gender, age, size, social, active, friendly, profilePic)
        self.redirect('/profile-view')
class ViewDogHandler(webapp2.RequestHandler):
    def get(self, dog_id):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_template_parameters()
            profile = data.get_user_profile(get_user_email())
            dog_key = ndb.Key(urlsafe=dog_id)
            dog = dog_key.get()
            values["name"] = dog.name
            values["breed"] = dog.breed
            values["gender"] = dog.gender
            values["age"] = dog.age
            values["size"] = dog.size
            values["social"] = dog.socialLevel
            values["active"] = dog.activityLevel
            values["friendly"] = dog.friendlyLevel
            values["keyUrl"] = dog_id
            localDogs = data.get_local_dogs(get_user_email(), profile.city, profile.state)
            print(localDogs)
            scoredDogs = []
            for d in localDogs:
                d.score = data.score_dog(dog ,d)
                d.keyUrl = d.key.urlsafe()
                scoredDogs.append(d)
            scoredDogs.sort(key=lambda d: d.score, reverse=True)
            values["matchedDogs"] = scoredDogs
            render_template(self, 'view-dog.html', values)



class Image(webapp2.RequestHandler):
    def get(self):
        dog_key = ndb.Key(urlsafe=self.request.get('img_id'))
        dog = dog_key.get()
        if dog.profilePic:
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(dog.profilePic)
        else:
            self.response.out.write('No image')

app = webapp2.WSGIApplication([
    ('/profile-view', ProfileViewHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/profile-edit', ProfileEditHandler),
    ('/add-dog', AddDogHandler),
    ('/view-dog/(.*)', ViewDogHandler),
    ('/img', Image),
    ('.*', MainHandler)
    ])
