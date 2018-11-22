from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName

api.templatedir('templates')

class StartseiteView(api.Page):
    api.context(Interface)

    def update(self):
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.login = portal + '/login'
        self.register = portal + '/@@register'
        if not ploneapi.user.is_anonymous():
            current = ploneapi.user.get_current()
            username = current.id
            roles = ploneapi.user.get_roles(username=username)
            if not 'Manager' in roles and not 'Site Administrator' in roles:
                pm = getToolByName(self.context, 'portal_membership')
                homeurl = pm.getHomeUrl()
                return self.request.response.redirect(homeurl)
