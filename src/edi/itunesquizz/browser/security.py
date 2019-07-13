# -*- coding: utf-8 -*-
from zope.interface import Interface
from plone import api as ploneapi
import zExceptions
from Products.Five import BrowserView

def checkOwner(context, request):
    if not ploneapi.user.is_anonymous():
        current = ploneapi.user.get_current()
        secroles = ['Manager', 'Owner',]
        currentroles = ploneapi.user.get_roles(username=current.id, obj=context)
        match = [x for x in secroles if x in currentroles]
        if match:
            return True
    return False

class SecurityPage(BrowserView):
    """Security Page""""
