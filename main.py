#!/usr/bin/env python
#
# account-manager - Ivan Martinez Estevez (04/2019)
#

from Controllers.add import AddHandler
from Controllers.showall import ListHandler
from Controllers.showcurrent import ShowcurrentHandler
from Controllers.edit import EditHandler
from Controllers.delete import DeleteHandler
from Controllers.delete import DeleteAllHandler
from Controllers.search import SearchHandler
from Controllers.error import ErrorHandler
from Controllers.image import ImageHandler

from google.appengine.api import users
from Models.movement import Movement
from jinja import JINJA_ENVIRONMENT

import webapp2
import datetime

Months = 12
Days_month = 30
Days_year = 365
Days_week = 7


class MainHandler(webapp2.RequestHandler):
    def load_data(self):
        if self.user:
            self.movements = Movement.query(Movement.user == self.user.user_id()).order(-Movement.date)
        else:
            self.movements = Movement.query().order(-Movement.date)

        self.today = datetime.date.today()
        today_format = str(self.today).split('-')
        self.today_str = str(today_format[2] + "/" + today_format[1] + "/" + today_format[0])

    def get(self):
        self.user = users.get_current_user()
        self.load_data()  # Loads the BD content

        if self.user:
            self.logout = users.create_logout_url("/")
            self.calulate_total()
            template_values = {
                'amount': self.total_amount,
                'logout': self.logout,
                'user': self.user.nickname(),
                'today': self.today_str,
                'movements': self.movements
            }
            template = JINJA_ENVIRONMENT.get_template("/Templates/index.html")
            self.response.write(template.render(template_values))
        else:
            login = users.create_login_url('/')
            template_values = {
                'login': login,
                'today': self.today_str,
            }
            template = JINJA_ENVIRONMENT.get_template("/Templates/login.html")
            self.response.write(template.render(template_values))

    def calulate_total(self):
        self.total_amount = 0

        for movement in self.movements:
            if movement.frequency == 'only':
                self.total_amount += movement.amount * self.calculate_completed(movement.date)
            elif movement.frequency == 'daily':
                self.total_amount += movement.amount * self.calculate_days(movement.date)
            elif movement.frequency == 'weekly':
                self.total_amount += movement.amount * self.calculate_weeks(movement.date)
            elif movement.frequency == 'monthly':
                self.total_amount += movement.amount * self.calculate_months(movement.date)
            elif movement.frequency == 'yearly':
                self.total_amount += movement.amount * self.calculate_years(movement.date)

    def calculate_completed(self, date):
        days = 0
        if date <= self.today:
            days = 1
        return days

    def calculate_days(self, date):
        days = 0
        if date <= self.today:
            diff = self.today - date
            days = diff.days + 1
        return days

    def calculate_weeks(self, date):
        days = 0
        if date <= self.today:
            diff = self.today - date
            days = (diff.days / Days_week) + 1
        return days

    def calculate_months(self, date):
        days = 0
        if date <= self.today:
            diff = self.today - date
            days = (diff.days / Days_month) + 1
        return days

    def calculate_years(self, date):
        days = 0
        if date <= self.today:
            diff = self.today - date
            days = (diff.days / Days_year) + 1
        return days


app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/add", AddHandler),
    ("/showall", ListHandler),
    ("/showcurrent", ShowcurrentHandler),
    ("/edit", EditHandler),
    ("/delete", DeleteHandler),
    ("/deleteAll", DeleteAllHandler),
    ("/search", SearchHandler),
    ("/error", ErrorHandler),
    ("/image", ImageHandler)
], debug=True)
