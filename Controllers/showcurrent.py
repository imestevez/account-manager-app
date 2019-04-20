# Showcurrent - Used to handler the current Movement

from jinja import JINJA_ENVIRONMENT
from Models.movement import frequency

from google.appengine.ext import ndb, db
import os
import webapp2
import datetime
import time


class ShowcurrentHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id is None:
            self.redirect("/error?msg=Movement was not found")
            return
        try:
            movement = ndb.Key(urlsafe=id).get()
        except:
            self.redirect("/error?msg=key does not exist")

        date_split = str(movement.date).split('-')
        template_values = {
            'movement': movement,
            'frequency': frequency,
            'blob': movement.invoice,
            'date': str(date_split[2] + "/" + date_split[1] + "/" + date_split[0])
        }
        template = JINJA_ENVIRONMENT.get_template("/Templates/showcurrent.html")
        self.response.write(template.render(template_values))
