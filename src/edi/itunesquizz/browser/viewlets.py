from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName
from edi.itunesquizz import hilfen
from edi.itunesquizz.kursordner import IKursordner
from plone.app.layout.viewlets.interfaces import IGlobalStatusMessage
from plone.app.layout.viewlets.interfaces import IAboveContentTitle
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

class HilfeViewlet(api.Viewlet):
    api.context(Interface)
    api.viewletmanager(IGlobalStatusMessage)

    def loggedin(self):
       if not ploneapi.user.is_anonymous():
           return True
       return False

    def checkhilfe(self):
        if hasattr(self.context, 'layout'):
            if self.context.layout == 'startseiteview' and ploneapi.user.is_anonymous():
                return hilfen.startseite

        if not ploneapi.user.is_anonymous():
            pm = getToolByName(self.context, 'portal_membership')
            homeurl = pm.getHomeUrl()
            if self.context.absolute_url() == homeurl:
                return hilfen.meinordner

        if self.context.portal_type == 'Folder' and self.request.getURL().endswith('++add++Kursordner'):
            return hilfen.aufgabenordner
        if self.context.portal_type == 'Kursordner' and self.request.getURL().endswith('@@edit'):
            return hilfen.aufgabenordner

        if self.context.portal_type == 'Kursordner' and self.request.getURL().endswith('++add++Aufgabe'):
            return hilfen.uebung
        if self.context.portal_type == 'Aufgabe' and self.request.getURL().endswith('@@edit'):
            return hilfen.uebung

        if self.context.portal_type == 'Kursordner' and self.request.getURL().endswith('++add++Experiment'):
            return hilfen.experiment
        if self.context.portal_type == 'Experiment' and self.request.getURL().endswith('@@edit'):
            return hilfen.experiment

        if self.context.portal_type == 'Kursordner' and self.request.getURL().endswith('++add++Arbeitsblatt'):
            return hilfen.arbeitsblatt
        if self.context.portal_type == 'Arbeitsblatt' and self.request.getURL().endswith('@@edit'):
            return hilfen.arbeitsblatt

        if self.context.portal_type == 'Arbeitsblatt':
            return hilfen.arbeitsblattansicht

        if self.context.portal_type == 'Kursordner':
            return hilfen.aufgabenliste

        if self.context.portal_type == 'Aufgabe':
            return hilfen.uebungsansicht

        if self.context.portal_type == 'Experiment':
            return hilfen.experimentansicht

        return False

    def update(self):
       self.hilfe = self.checkhilfe()
       self.logoutlink = ploneapi.portal.get().absolute_url() + '/logout'
