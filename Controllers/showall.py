# Showall - Used to show all Movements of the user

from jinja import JINJA_ENVIRONMENT
from Models.movement import Movement
from Models.movement import frequency
import webapp2


class ListHandler(webapp2.RequestHandler):
    def get(self):
        self.movements = Movement.query().order(-Movement.date)
        self.dates = dict()  # Creates a dictionary to store the dates with format dd/mm/yyy
        self.date_format()  # Call to refill dates dictionary

        template_values = {
            'frequency': frequency,
            'movements': self.movements,
            'dates': self.dates,
            'numMovements': self.movements.count()
        }
        template = JINJA_ENVIRONMENT.get_template("/Templates/showall.html")
        self.response.write(template.render(template_values))

    def date_format(self):
        for movement in self.movements:
            date_split = str(movement.date).split('-')
            self.dates[movement.key] = str(date_split[2] + "/" + date_split[1] + "/" + date_split[0])
