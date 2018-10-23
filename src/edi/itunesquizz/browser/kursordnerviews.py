from zope.interface import Interface
from uvc.api import api

api.templatedir('templates')

class KursordnerView(api.Page):
    api.context(Interface)

