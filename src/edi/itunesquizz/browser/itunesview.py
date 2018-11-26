from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi

api.templatedir('templates')

class iTunesView(api.View):
    api.context(Interface)

    def update(self):
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.webcode = self.request.get('code')
        self.setterurl = portal + '/@@cookiesetter'
        if self.webcode:
            brains = ploneapi.content.find(Webcode=self.webcode)
            obj = brains[0].getObject()
            if obj.portal_type == 'Aufgabe':
                viewextension = u'/@@aufgabeitunes'
            elif obj.portal_type == 'Experiment':
                viewextension = u'/@@experimentitunes'
            if obj.art == 'selbsttest':
                return self.redirect(obj.absolute_url() + viewextension)
            else:
                sdm = self.context.session_data_manager
                session = sdm.getSessionData(create=True)
                if session.has_key('usermail'):
                    return self.redirect(obj.absolute_url() + viewextension)
        else:
            print 'return to error-site'


class CookieSetter(api.View):
    api.context(Interface)

    def render(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("usermail", self.request.form.get('email'))
        url = ploneapi.portal.get().absolute_url() + '/@@itunesview?code=' + self.request.form.get('webcode')
        return self.redirect(url)
