from zope.interface import Interface
from plone import api as ploneapi
from plone.app.contenttypes.interfaces import ICollection
from Products.CMFCore.interfaces import IFolderish
from plone import api as ploneapi
from edi.itunesquizz.leermeldungen import startseite
from edi.itunesquizz.browser.security import checkOwner
from Products.Five import BrowserView

class MeinOrdnerView(BrowserView):

    @property
    def query(self):
        """ 
        Make catalog query for the folder listing.
        """
        if ICollection.providedBy(self.context):
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
