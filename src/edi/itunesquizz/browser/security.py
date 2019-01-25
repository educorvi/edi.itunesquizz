# -*- coding: utf-8 -*-
from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
import zExceptions

api.templatedir('templates')

#class NotFound(api.View):
#    api.context(zExceptions.NotFound)
#    api.name("index.html")
#
#    def render(self):
#        self.request.response.status = "404"
#        return u"NOT FOUND"

def checkOwner(context, request):
    if not ploneapi.user.is_anonymous():
        current = ploneapi.user.get_current()
        secroles = ['Manager', 'Owner',]
        currentroles = ploneapi.user.get_roles(username=current.id, obj=context)
        match = [x for x in secroles if x in currentroles]
        if match:
            return True
    return False

class SecurityPage(api.Page):
    api.context(Interface)
