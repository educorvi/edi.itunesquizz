from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from pymongo import MongoClient

api.templatedir('templates')

class iTunesView(api.View):
    api.context(Interface)

    def update(self):
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.webcode = self.request.get('code')
        if self.webcode:
            brains = ploneapi.content.find(Webcode=self.webcode)
            obj = brains[0].getObject()
            if obj.portal_type == 'Aufgabe':
                viewextension = u'/@@aufgabeitunes'
            elif obj.portal_type == 'Experiment':
                viewextension = u'/@@experimentitunes'
            elif obj.portal_type == 'Arbeitsblatt':
                viewextension = u'/@@arbeitsblattitunes'
            return self.redirect(obj.absolute_url() + viewextension)
        else:
            print 'return to error-site'

class ITunes_Aufgabe_Validation(api.View):
    api.context(Interface)

    def update(self):
        dbid = self.request.get('id')
        client = MongoClient('localhost', 27017)
        db = client.itunesu
        collection = db.quizzes
        data = collection.find_one({"_id": dbid})
        return data

class ITunes_Experiment_Validation(ITunes_Aufgabe_Validation):
    api.context(Interface)

class ITunes_Arbeitsblatt_Validation(ITunes_Aufgabe_Validation):
    api.context(Interface)


class CookieSetter(api.View):
    api.context(Interface)

    def render(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("usermail", self.request.form.get('email'))
        url = ploneapi.portal.get().absolute_url() + '/@@itunesview?code=' + self.request.form.get('webcode')
        return self.redirect(url)
