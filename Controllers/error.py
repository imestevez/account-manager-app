# Error - Used to handler the errors produced

from jinja import JINJA_ENVIRONMENT
from google.appengine.api import users

import webapp2


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        self.user = users.get_current_user()
        if self.user:
            logout = users.create_logout_url("/")
            msg = None
            try:
                msg = self.request.GET['msg']
            except:
                msg = None

            if msg is None:
                msg = "CRITICAL - contact development team"

            template_values = {
                "msg": msg,
                'logout': logout
            }

            template = JINJA_ENVIRONMENT.get_template("/Templates/error.html")
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')