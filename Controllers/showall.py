# Showall - Used to show all Movements of the user

from jinja import JINJA_ENVIRONMENT
from google.appengine.api import users
from Models.movement import Movement
from Models.movement import frequency
import datetime
import webapp2

Months = 12
Days_month = 30
Days_year = 365
Days_week = 7


class ListHandler(webapp2.RequestHandler):
    def get(self):
        self.today = datetime.date.today()

        self.user = users.get_current_user()
        if self.user:  # If there is user
            logout = users.create_logout_url("/")
            self.movements = Movement.query(Movement.user == self.user.user_id()).order(-Movement.date)
            self.dates = dict()  # Creates a dictionary to store the dates with format dd/mm/yyy
            self.calulate_total()
            self.date_format()  # Call to refill dates dictionary
            template_values = {
                'frequency': frequency,
                'movements': self.movements,
                'total': self.total_Movements,
                'dates': self.dates,
                'numMovements': self.movements.count(),
                'logout': logout
            }
            template = JINJA_ENVIRONMENT.get_template("/Templates/showall.html")
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def calulate_total(self):
        self.total_Movements = {}
        total_amount = 0
        for movement in self.movements:
            if movement.frequency == 'only':
                total_amount = movement.amount * self.calculate_completed(movement.date)
            elif movement.frequency == 'daily':
                total_amount = movement.amount * self.calculate_days(movement.date)
            elif movement.frequency == 'weekly':
                total_amount = movement.amount * self.calculate_weeks(movement.date)
            elif movement.frequency == 'monthly':
                total_amount = movement.amount * self.calculate_months(movement.date)
            elif movement.frequency == 'yearly':
                total_amount = movement.amount * self.calculate_years(movement.date)
            self.total_Movements[movement.key] = total_amount

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

    def date_format(self):
        for movement in self.movements:
            date_split = str(movement.date).split('-')
            self.dates[movement.key] = str(date_split[2] + "/" + date_split[1] + "/" + date_split[0])
