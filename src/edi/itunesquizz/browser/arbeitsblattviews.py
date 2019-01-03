from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from edi.itunesquizz.arbeitsblatt import IArbeitsblatt

api.templatedir('templates')

class ArbeitsblattITunes(api.View):
    api.context(IArbeitsblatt)


    def update(self):
        retdict = {}
        portal = ploneapi.portal.get().absolute_url()
        retdict['validationurl'] = self.context.absolute_url() + '/@@validatearbeitsblatt'
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        contentdir = []
        contentlist = []
        for i in self.context.parts:
            obj = ploneapi.content.get(UID=i)
            objview = obj.portal_type.lower() + 'itunes'
            objdict = ploneapi.content.get_view(objview, obj, self.request).update()
            objdict['type'] = obj.portal_type
            objdict['name'] = i
            contentdir.append((self.context.absolute_url()+'/@@arbeitsblattitunes/#'+i, obj.Title()))
            contentlist.append(objdict)
        retdict['contentdir'] = contentdir
        retdict['contentlist'] = contentlist
        return retdict

class ValidateArbeitsblatt(api.View):
    api.context(IArbeitsblatt)


    def update(self):
        resultdict = self.request.form
        del resultdict['_authenticator']
        elements = {}
        for i in resultdict:
            if i.startswith('reihe'):
                parts = i.split('_')
                keyid = ploneapi.content.get(UID=parts[1]).id
                if not elements.has_key(keyid):
                    elements[keyid] = {}
                elements[keyid][i] = resultdict.get(i)
            else:
                elements[i] = resultdict.get(i)
        contentdir = []
        contentlist = []
        for i in self.context.parts:
            obj = ploneapi.content.get(UID=i)
            objview = 'validate' + obj.portal_type.lower()
            validation = ploneapi.content.get_view(objview, obj, self.request)
            print validation
            #Extrahieren der Results aus dem Elemente Dictionary
            result = elements.get(obj.id)
            if obj.portal_type == 'Aufgabe':
                resultdict = validation.formatoutputs({obj.id:result})
                contentlist.append(resultdict)
            elif obj.portal_type == 'Experiment':
                formkeys = result.keys()
                formkeys.sort()
                resultdict = validation.formatoutputs(formkeys, result)
                contentlist.append(resultdict)
        import pdb;pdb.set_trace()
        print contentlist
            
    def render(self):
        
        return u'ok'


class ArbeitsblattView(api.Page):
    api.context(IArbeitsblatt)

    def update(self):
        self.kursordner = self.context.aq_parent.absolute_url()
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        #self.aufgabenart = aufgabenart.getTerm(self.context.art).title
        if self.context.webcode:
            self.ituneslink = portal + '/@@itunesview?code=' + self.context.webcode
        else:
            self.ituneslink = self.context.absolute_url() + '/@@arbeitsblattitunes'
        self.parts = []
        for i in self.context.parts:
            entry = {}
            obj = ploneapi.content.get(UID=i)
            entry['title'] = obj.title
            entry['url'] = obj.absolute_url()
            self.parts.append(entry)
