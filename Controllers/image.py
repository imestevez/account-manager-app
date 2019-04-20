# Image - Used to show the images

from google.appengine.ext import ndb

import webapp2


class ImageHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['id']
        except:
            id = None

        if id is None:
            self.redirect("/error?msg=Movement was not found")
            return
        try:
            movement = ndb.Key(urlsafe=id).get()
        except:
            self.redirect("/error?msg=key does not exist")
            return
        if movement.invoice:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(movement.invoice)
