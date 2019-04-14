from jinja import JINJA_ENVIRONMENT
import webapp2


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("/Templates/login.html")
        self.response.write(template.render())
