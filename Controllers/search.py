# Search - Used to search the Movements by date, type or frequency

from jinja import JINJA_ENVIRONMENT
from Models.movement import frequency
from Models.movement import Movement
from google.appengine.api import users

import webapp2
import datetime
import time

Months = 12
Days_month = 30
Days_year = 365
Days_week = 7


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        self.user = users.get_current_user()
        if self.user:
            template_values = {
                'today': datetime.date.today()
            }
            template = JINJA_ENVIRONMENT.get_template("/Templates/search.html")
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        self.today = datetime.date.today()

        self.user = users.get_current_user()
        if self.user:
            logout = users.create_logout_url("/")

            self.movs_list = list()  # List for send the movements to the view
            self.dates = dict()  # Creates a dictionary to store the dates with format dd/mm/yyy

            self.type = self.request.get('type').strip()
            self.frequency = self.request.get('frequency').strip()
            try:
                date_i = self.request.get("dateInit").strip().split("-")
                self.dateInit = datetime.date(int(date_i[0]), int(date_i[1]), int(date_i[2]))
            except:
                self.dateInit = ""
            try:
                date_e = self.request.get("dateEnd").strip().split("-")
                self.dateEnd = datetime.date(int(date_e[0]), int(date_e[1]), int(date_e[2]))
            except:
                self.dateEnd = ""

            self.search()  # Searches the mathing parameters
            self.date_format()  # Call to refill dates dictionary
            self.calulate_total()

            template_values = {
                'frequency': frequency,
                'movements': self.movs_list,
                'dates': self.dates,
                'total': self.total_Movements,
                'numMovements': len(self.movs_list),
                'logout': logout,
                'search': True
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

    def search(self):
        self.movements = Movement.query(Movement.user == self.user.user_id())
        if self.frequency != "":  # If frequency isn't empty
            self.movements = self.movements.filter(Movement.frequency == self.frequency)
        if self.type == 'deposit':
            self.movements = self.movements.filter(Movement.amount > 0)
        elif self.type == 'expense':
            self.movements = self.movements.filter(Movement.amount < 0)

        if self.dateInit != "" or self.dateEnd != "":  # If one of the both isn't empty
            self.filter_date()
        else:  # If Both are empty
            for movement in self.movements:
                self.movs_list.append(movement)  # Fill the list to send to view

    def filter_date(self):
        if self.dateInit == self.dateEnd != "":
            for movement in self.movements:
                if self.dateInit <= movement.date <= self.dateEnd:
                    self.movs_list.append(movement)
        else:
            if self.dateInit != "":
                for movement in self.movements:
                    if movement.date >= self.dateInit:
                        self.movs_list.append(movement)
            elif self.dateEnd != "":
                for movement in self.movements:
                    if movement.date <= self.dateEnd:
                        self.movs_list.append(movement)
