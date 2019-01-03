from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.interfaces import IPortalFooter

api.templatedir('templates')

class LoggedInMembers(api.Viewlet):
    api.context(Interface)
    api.viewletmanager(IPortalFooter)

    def update(self):
        self.available = True
        if not ploneapi.user.is_anonymous():
            current = ploneapi.user.get_current()
            editroles = [u'Manager', u'Site Administrator']
            pm = getToolByName(self.context, 'portal_membership')
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            match = [x for x in editroles if x in roles]
            if match:
                self.available = False

class LoggedInAll(api.Viewlet):
    api.context(Interface)
    api.viewletmanager(IPortalFooter)

    def update(self):
        self.available = True
