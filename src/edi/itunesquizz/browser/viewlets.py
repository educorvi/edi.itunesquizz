import random
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName
from edi.itunesquizz import hilfen
from edi.itunesquizz.kursordner import IKursordner
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets import ViewletBase


class BannerViewlet(ViewletBase):

    def render(self):
        registry = getUtility(IRegistry)
        try:
            if not registry['edi.itunesquizz.settings.IQuizSettings.isquizsite']:
                return ''
        except:
            return ''
        portal = ploneapi.portal.get()
        if self.context == portal:
            return super(BannerViewlet, self).render()
        return ''

    def update(self):
        portal = ploneapi.portal.get().absolute_url()
        background = u"background-image:url('%s');background-size:cover;min-height:400px;max-height:400px;background-repeat:no-repeat"
        topimage = portal + '/++resource++edi.itunesquizz/images/default-top.jpg'
        self.topstyle = background %topimage
        registry = getUtility(IRegistry)
        topexamples = []
        try:
            topexamples = ploneapi.content.find(UID=registry['edi.itunesquizz.settings.IQuizSettings.topexamples'])
        except:
            topexamples = []
        objdict = {}
        if topexamples:
            index = random.randint(1,len(topexamples)) - 1
            topaufgabe = topexamples[index].UID
            obj = ploneapi.content.get(UID=topaufgabe)
            objview = obj.portal_type.lower() + 'plone'
            objdict = ploneapi.content.get_view(objview, obj, self.request).update()
            objdict['type'] = obj.portal_type
            objdict['name'] = topaufgabe
            self.topstyle = background %objdict['bild']
        self.objdict = objdict


class LoggedInMembers(ViewletBase):

    def checker(self):
        registry = getUtility(IRegistry)
        try:
            if not registry['edi.itunesquizz.settings.IQuizSettings.isquizsite']:
                return False
        except:
            return False
        if not ploneapi.user.is_anonymous():
            current = ploneapi.user.get_current()
            editroles = [u'Manager', u'Site Administrator']
            pm = getToolByName(self.context, 'portal_membership')
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            match = [x for x in editroles if x in roles]
            if match:
                return False
        return True

    def render(self):
        if not self.checker():
            return ''
        return super(LoggedInMembers, self).render()


class HilfeViewlet(ViewletBase):

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
        self.login = self.loggedin()
        self.logoutlink = ploneapi.portal.get().absolute_url() + '/logout'
        self.loginlink = ploneapi.portal.get().absolute_url() + '/login'
        self.reglink = ploneapi.portal.get().absolute_url() + '/register'

    def render(self):
        registry = getUtility(IRegistry)
        try:
            if not registry['edi.itunesquizz.settings.IQuizSettings.isquizsite']:
                return ''
        except:
            return ''
        return super(HilfeViewlet, self).render()
