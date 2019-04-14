#!/usr/bin/env python
#
# movement-manager - Ivan Martinez Estevez (04/2019)
#

from Controllers.login import LoginHandler
from Controllers.add import AddHandler
from Controllers.showall import ListHandler
from Controllers.showcurrent import ShowcurrentHandler
from Controllers.edit import EditHandler
from Controllers.delete import DeleteHandler
from Controllers.search import SearchHandler
from Controllers.error import ErrorHandler

from Models.movement import Movement
from jinja import JINJA_ENVIRONMENT

import webapp2
import datetime

Months = 12
Days_month = 30
Days_year = 365
Weeks_year = Months * 4


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.total_amount = 0
        self.today = datetime.date.today()
        self.load_data()  # Loads the BD content
        self.calulate_total()
        today_format = str(self.today).split('-')
        template_values = {
            'amount': self.total_amount,
            'today': str(today_format[2] + "/" + today_format[1] + "/" + today_format[0]),
            'movements': self.movements
        }
        template = JINJA_ENVIRONMENT.get_template("/Templates/index.html")
        self.response.write(template.render(template_values))

    def calulate_total(self):
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
        if date < self.today:
            days = 1
        return days

    def calculate_days(self, date):
        days = 0
        if date < self.today:
            diff = self.today - date
            days = diff.days + 1
        return days

    def calculate_weeks(self, date):
        days = 0
        if date < self.today:
            diff = self.today - date
            days = (diff.days / Weeks_year) + 1
        return days

    def calculate_months(self, date):
        days = 0
        if date < self.today:
            diff = self.today - date
            days = (diff.days / Days_month) + 1
        return days

    def calculate_years(self, date):
        days = 0
        if date < self.today:
            diff = self.today - date
            days = (diff.days / Days_year) + 1
        return days

    def load_data(self):
        self.movements = Movement.query().order(-Movement.date)


app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/login", LoginHandler),
    ("/add", AddHandler),
    ("/add", AddHandler),
    ("/showall", ListHandler),
    ("/showcurrent", ShowcurrentHandler),
    ("/edit", EditHandler),
    ("/delete", DeleteHandler),
    ("/search", SearchHandler),
    ("/error", ErrorHandler)

], debug=True)
