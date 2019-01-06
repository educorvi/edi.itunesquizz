from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName

api.templatedir('templates')

class StartseiteView(api.Page):
    api.context(Interface)

    def getexamples(self):
        examples = {}
        portal_url = ploneapi.portal.get().absolute_url()
        ex_context = ploneapi.portal.get()['beispiele']
        experimente = ploneapi.content.find(context=ex_context, portal_type='Experiment')
        experiment = experimente[0].getObject()
        examples['experiment'] = {'url':experiment.absolute_url() + '/@@experimentitunes', 'title':experiment.title, 
                                  'img': '%s/@@images/image/preview' % experiment.absolute_url()}
        aufgaben = ploneapi.content.find(context=ex_context, portal_type='Aufgabe')
        aufgabe = aufgaben[0].getObject()
        examples['aufgabe'] = {'url':aufgabe.absolute_url() + '/@@aufgabeitunes', 'title':aufgabe.title, 
                               'img': '%s/@@images/image/preview' % aufgabe.absolute_url()}
        arbeitsblaetter = ploneapi.content.find(context=ex_context, portal_type='Arbeitsblatt')
        arbeitsblatt = arbeitsblaetter[0].getObject()
        examples['arbeitsblatt'] = {'url':arbeitsblatt.absolute_url() + '/@@arbeitsblattitunes', 'title':arbeitsblatt.title,
                               'img': '%s/arbeitsblatt.png' % portal_url}
        return examples


    def update(self):
        self.examples = self.getexamples()
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
