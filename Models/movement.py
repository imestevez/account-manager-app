# Movement
# Used for store the movemets data

from google.appengine.ext import ndb

frequency = {'only': 'Puntual',
             'daily': 'Diario',
             'weekly': 'Semanal',
             'monthly': 'Mensual',
             'yearly': 'Anual'}


class Movement(ndb.Model):
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    invoice = ndb.StringProperty()
    date = ndb.DateProperty(required=True)
    amount = ndb.FloatProperty(required=True)
    frequency = ndb.StringProperty(required=True)
