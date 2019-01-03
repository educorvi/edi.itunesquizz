from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from Products.ATContentTypes.interface import IATTopic
from plone.app.contenttypes.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish
from plone import api as ploneapi
from edi.itunesquizz.leermeldungen import startseite

api.templatedir('templates')

class MeinOrdnerView(api.Page):
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

    def update(self):
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.leermeldung = startseite
        self.meinordner = self.context.aq_parent.absolute_url()
        self.kursordner = []
        self.inhalte = False
        brains = self.query
        for i in brains:
            self.inhalte = True
            if i.portal_type == 'Kursordner':
                entry = {}
                entry['url'] = i.getURL()
                entry['title'] = i.Title
                entry['image'] = ''
                obj = i.getObject()
                if obj.image:
                    entry['image'] = "%s/@@images/image/tile" % obj.absolute_url()
                entry['description'] = i.Description
                self.kursordner.append(entry)
