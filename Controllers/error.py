# Error - Used to handler the errors produced

from jinja import JINJA_ENVIRONMENT
from Models.movement import Movement
from Models.movement import frequency
import webapp2


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        msg = None
        try:
            msg = self.request.GET['msg']
        except:
            msg = None

        if msg is None:
            msg = "CRITICAL - contact development team"

        template_values = {
            "msg": msg,
        }

        template = JINJA_ENVIRONMENT.get_template("/Templates/error.html")
        self.response.write(template.render(template_values))
