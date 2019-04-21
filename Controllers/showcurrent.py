# Showcurrent - Used to handler the current Movement

from jinja import JINJA_ENVIRONMENT
from Models.movement import frequency

from google.appengine.ext import ndb, db
from google.appengine.api import users

import webapp2


class ShowcurrentHandler(webapp2.RequestHandler):
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

            date_split = str(movement.date).split('-')
            template_values = {
                'movement': movement,
                'frequency': frequency,
                'blob': movement.invoice,
                'date': str(date_split[2] + "/" + date_split[1] + "/" + date_split[0]),
                'logout': logout
            }
            template = JINJA_ENVIRONMENT.get_template("/Templates/showcurrent.html")
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')