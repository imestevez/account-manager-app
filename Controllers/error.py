# Error - Used to handler the errors produced

from jinja import JINJA_ENVIRONMENT
from Models.movement import Movement
from Models.movement import frequency
import webapp2


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        errorMessage = None
        try:
            errorMessage = self.request.GET['errorMessage']
        except:
            msg = None

        if msg is None:
            errorMessage = "CRITICAL - contact development team"

        template_values = {
            "errorMessage": errorMessage,
        }

        template = JINJA_ENVIRONMENT.get_template("/Templates/error.html")
        self.response.write(template.render(template_values))
