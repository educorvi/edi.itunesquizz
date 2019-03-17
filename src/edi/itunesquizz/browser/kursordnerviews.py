from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from Products.ATContentTypes.interface import IATTopic
from plone.app.contenttypes.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish
from plone import api as ploneapi
from edi.itunesquizz.leermeldungen import aufgabenordner
from edi.itunesquizz.browser.security import checkOwner

api.templatedir('templates')

class KursordnerView(api.Page):
    api.context(Interface)

    @property
    def query(self):
        """ 
        Make catalog query for the folder listing.
        """
        if IATTopic.providedBy(self.context):
            q = self.context.buildQuery()
            pcat = getToolByName(self.context, 'portal_catalog')
            return pcat.searchResults(q)
        elif ICollection.providedBy(self.context):
            return self.context.queryCatalog(batch=False)
        elif IFolderish.providedBy(self.context):
            return self.context.getFolderContents(batch=False)

    def editpanel(self):
        if not ploneapi.user.is_anonymous():
            current = ploneapi.user.get_current()
            editroles = ['Manager', 'Owner', 'Editor']
            currentroles = ploneapi.user.get_roles(username=current.id, obj=self.context)
            match = [x for x in editroles if x in currentroles]
            if match:
                return True
        return False

    def update(self):
        if not checkOwner(self.context, self.request):
            self.request.response.redirect(self.context.absolute_url() + '/@@securitypage')
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.meinordner = self.context.aq_parent.absolute_url()
        self.leermeldung = aufgabenordner
        self.uebungen = []
        self.bilder = []
        self.experimente = []
        self.arbeitsblaetter = []
        self.vokabeltests = []
        self.inhalte = False
        brains = self.query
        for i in brains:
            self.inhalte = True
            if i.portal_type == 'Aufgabe':
                entry = {}
                entry['url'] = i.getURL()
                entry['title'] = i.Title
                self.uebungen.append(entry)
            if i.portal_type == 'Experiment':
                entry = {}
                entry['url'] = i.getURL()
                entry['title'] = i.Title
                self.experimente.append(entry)
            if i.portal_type == 'Arbeitsblatt':
                entry = {}
                entry['url'] = i.getURL()
                entry['title'] = i.Title
                self.arbeitsblaetter.append(entry)
            if i.portal_type == 'Vokabeltest':
                entry = {}
                entry['url'] = i.getURL()
                entry['title'] = i.Title
                self.vokabeltests.append(entry)
            elif i.portal_type == 'Image':
                entry = {}
                entry['url'] = i.getURL()
                entry['image'] = '%s/@@images/image/mini' % i.getURL()
                entry['title'] = i.Title
                self.bilder.append(entry)
