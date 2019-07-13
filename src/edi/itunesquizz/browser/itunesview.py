from zope.interface import Interface
from plone import api as ploneapi
from pymongo import MongoClient
from Products.Five import BrowserView

class iTunesView(BrowserView):

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
            elif obj.portal_type == 'Vokabeltest':
                viewextension = u'/@@vokabeltestitunes'
            elif obj.portal_type == 'Vokabelserie':
                viewextension = u'/@@vokabelserieitunes'
            return self.redirect(obj.absolute_url() + viewextension)
        else:
            print 'return to error-site'

class ITunes_Aufgabe_Validation(BrowserView):

    def update(self):
        dbid = self.request.get('id')
        client = MongoClient('localhost', 27017)
        db = client.itunesu
        collection = db.quizzes
        data = collection.find_one({"_id": dbid})
        return data

class ITunes_Experiment_Validation(ITunes_Aufgabe_Validation):
    """Validation Klass"""

class ITunes_Arbeitsblatt_Validation(ITunes_Aufgabe_Validation):
    """Validation Klass"""

class CookieSetter(BrowserView):

    def __call__(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("usermail", self.request.form.get('email'))
        url = ploneapi.portal.get().absolute_url() + '/@@itunesview?code=' + self.request.form.get('webcode')
        return self.redirect(url)
