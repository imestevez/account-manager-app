# Edit - Used to edit a movement

from jinja import JINJA_ENVIRONMENT

from google.appengine.ext import ndb, db
from google.appengine.api import users

import webapp2
import datetime
import time


class EditHandler(webapp2.RequestHandler):
    def get(self):
        self.user = users.get_current_user()
        if self.user:
            logout = users.create_logout_url("/")
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
                return

            template_values = {
                'movement': movement,
                'logout': logout
            }
            template = JINJA_ENVIRONMENT.get_template("/Templates/edit.html")
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
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

        movement.title = self.request.get("title").strip()
        movement.amount = float(self.request.get("amount").strip())
        invoice = self.request.get("invoice_new").strip()
        if invoice:
            movement.invoice = db.Blob(invoice)
        movement.description = self.request.get("description").strip()
        movement.frequency = self.request.get("frequency").strip()
        date = self.request.get("date").strip().split("-")
        movement.date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))

        type = self.request.get("type").strip()
        if type == "deposit":  # if is a deposit
            if movement.amount < 0:  # if is less than 0
                movement.amount *= -1
        elif type == "expense":  # if is an expense
            if movement.amount > 0:  # if is greater than 0
                movement.amount *= -1

        movement.put()

        # Save
        time.sleep(1)  # wait for updates
        self.redirect("/")
