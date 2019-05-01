# Delete - Used to delete a movement

from Models.movement import Movement
from jinja import JINJA_ENVIRONMENT
from google.appengine.ext import ndb
from google.appengine.api import users

import webapp2
import datetime
import time


class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        self.user = users.get_current_user()
        if self.user:
            logout = users.create_logout_url("/")
            try:
                id = self.request.GET['id']  # Get the id from view
            except:
                id = None

            if id is None:
                self.redirect("/error?msg=Movement id was missed")
                return
            try:
                movement = ndb.Key(urlsafe=id).get()  # Get the movement object
            except:
                self.redirect("/error?msg=There isn't any movement with the sent id")
                return

            template_values = {
                'movement': movement,
                'logout': logout
            }
            template = JINJA_ENVIRONMENT.get_template("/Templates/delete.html")
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        self.user = users.get_current_user()
        if self.user: # If there is user
            try:
                id = self.request.GET['id']
            except:
                id = None

            if id == None:
                self.redirect("/error?msg=Movement was not found")
                return
            try:
                movement = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            movement.key.delete()
            # Save
            time.sleep(1)  # wait for updates
            self.redirect("/")
        else:
            self.redirect("/")


class DeleteAllHandler(webapp2.RequestHandler):
    def get(self):
        self.user = users.get_current_user()
        if self.user:
            logout = users.create_logout_url('/')
            movements = Movement.query(Movement.user == self.user.user_id())  # Gets all movents
            template_values = {
                'movements': movements.count(),
                'logout': logout
            }

            template = JINJA_ENVIRONMENT.get_template("/Templates/deleteAll.html")
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        self.user = users.get_current_user()
        if self.user:
            movements = Movement.query(Movement.user == self.user.user_id())  # Gets all movents
            for movement in movements:
                movement.key.delete()  # Deletes all movements

            # Save
            time.sleep(1)  # wait for updates
            self.redirect("/")
        else:
            self.redirect("/")
