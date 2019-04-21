from Models.movement import Movement
from jinja import JINJA_ENVIRONMENT
from google.appengine.ext import ndb

import webapp2
import datetime
import time


class DeleteHandler(webapp2.RequestHandler):
    def get(self):
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
        }
        template = JINJA_ENVIRONMENT.get_template("/Templates/delete.html")
        self.response.write(template.render(template_values))

    def post(self):
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


class DeleteAllHandler(webapp2.RequestHandler):
    def get(self):
        movements = Movement.query()  # Gets all movents
        template_values = {
            'movements': movements.count(),
        }

        template = JINJA_ENVIRONMENT.get_template("/Templates/deleteAll.html")
        self.response.write(template.render(template_values))

    def post(self):
        movements = Movement.query()  # Gets all movents
        num_Movements = movements.count()  # Counts the number of movents
        for movement in movements:
            movement.key.delete()  # Deletes all movements

        # Save
        time.sleep(1)  # wait for updates
        self.redirect("/")
