from Models.movement import Movement
from jinja import JINJA_ENVIRONMENT

from google.appengine.ext import ndb, db


import webapp2
import datetime
import time
import os
import shutil


class AddHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'today': datetime.date.today()
        }
        template = JINJA_ENVIRONMENT.get_template("/Templates/add.html")
        self.response.write(template.render(template_values))

    def post(self):
        movement = Movement()
        movement.title = self.request.get("title").strip()
        movement.amount = float(self.request.get("amount").strip())

        invoice = self.request.get("invoice").strip()
        if invoice != "":
            movement.invoice = db.Blob(invoice)
        else:
            movement.invoice = ""
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

    def save_file(self, name):
        pass
