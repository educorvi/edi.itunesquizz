from zope.interface import Interface
from plone import api as ploneapi
from edi.itunesquizz.arbeitsblatt import IArbeitsblatt
from edi.itunesquizz.browser.security import checkOwner
from Products.Five import BrowserView

def sizeof_fmt(num, suffix='Byte'):
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)

class ArbeitsblattITunes(BrowserView):

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
        if self.context.toc:
            #Inhaltsverzeichnis nur aktivieren wenn das Bool-Feld gesetzt ist
            retdict['contentdir'] = contentdir
        retdict['datei'] = {}
        if self.context.datei:
            datei = {}
            datei['url'] = "%s/@@download/datei/%s" %(self.context.absolute_url(), self.context.datei.filename)
            if self.context.datei.contentType.startswith('audio'):
                datei['contentType'] = 'audio/mpeg'
            else:
                datei['contentType'] = self.context.datei.contentType
            datei['size'] = sizeof_fmt(self.context.datei.size)
            datei['filename'] = self.context.datei.filename
            retdict['datei'] = datei
        illustration = ''
        if self.context.image:
            illustration = 'bild'
            retdict['bild'] = '%s/@@images/image' % self.context.absolute_url()
        if self.context.video:
            illustration = 'film'
            retdict['film'] = self.context.absolute_url()
        retdict['illustration'] = illustration
        retdict['contentlist'] = contentlist
        return retdict


class ArbeitsblattPlone(BrowserView):

    def update(self):
        retdict = {}
        portal = ploneapi.portal.get().absolute_url()
        retdict['validationurl'] = self.context.absolute_url() + '/@@validatearbeitsblattplone'
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        contentdir = []
        contentlist = []
        for i in self.context.parts:
            obj = ploneapi.content.get(UID=i)
            objview = obj.portal_type.lower() + 'itunes'
            objdict = ploneapi.content.get_view(objview, obj, self.request).update()
            objdict['type'] = obj.portal_type
            objdict['name'] = i
            contentdir.append((self.context.absolute_url()+'/@@arbeitsblattplone/#'+i, obj.Title()))
            contentlist.append(objdict)
        if self.context.toc:
            #Inhaltsverzeichnis nur aktivieren wenn das Bool-Feld gesetzt ist
            retdict['contentdir'] = contentdir
        retdict['datei'] = {}
        if self.context.datei:
            datei = {}
            datei['url'] = "%s/@@download/datei/%s" %(self.context.absolute_url(), self.context.datei.filename)
            if self.context.datei.contentType.startswith('audio'):
                datei['contentType'] = 'audio/mpeg'
            else:
                datei['contentType'] = self.context.datei.contentType
            datei['size'] = sizeof_fmt(self.context.datei.size)
            datei['filename'] = self.context.datei.filename
            retdict['datei'] = datei
        illustration = ''
        if self.context.image:
            illustration = 'bild'
            retdict['bild'] = '%s/@@images/image' % self.context.absolute_url()
        if self.context.video:
            illustration = 'film'
            retdict['film'] = self.context.absolute_url()
        retdict['illustration'] = illustration
        retdict['contentlist'] = contentlist
        return retdict


class ValidateArbeitsblatt(BrowserView):

    def cookiesetter(self, retdict):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("qrdata", retdict)

    def update(self):
        retdict = {}
        again = False
        resultdict = self.request.form
        if resultdict.has_key('_authenticator'):
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
            result = elements.get(obj.id)
            if obj.portal_type == 'Aufgabe':
                resultdict = validation.formatoutputs(result)
                resultdict = validation.formataufgabe(resultdict)
                if resultdict['again'] == True:
                    again = True
            elif obj.portal_type == 'Experiment':
                formkeys = result.keys()
                formkeys.sort()
                resultdict = validation.formatoutputs(formkeys, result)
                resultdict = validation.formatexperiment(resultdict)
                if resultdict['again'] == True:
                    again = True
            resultdict['type'] = obj.portal_type
            resultdict['name'] = i
            contentlist.append(resultdict)
            contentdir.append((self.context.absolute_url()+'/@@arbeitsblattitunes/#'+i, obj.Title()))
        retdict['contentlist'] = contentlist
        retdict['contentdir'] = contentdir
        portal = ploneapi.portal.get().absolute_url()
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['questionurl'] = self.context.absolute_url() + '/@@arbeitsblattitunes'
        retdict['again'] = again
        retdict['art'] = self.context.art
        if self.context.art == 'benotet':
            cookie = self.cookiesetter(retdict)
        return retdict

            
class ValidateArbeitsblattPlone(api.Page):
    api.context(IArbeitsblatt)

    def cookiesetter(self, retdict):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("qrdata", retdict)

    def update(self):
        retdict = {}
        again = False
        resultdict = self.request.form
        if resultdict.has_key('_authenticator'):
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
            result = elements.get(obj.id)
            if obj.portal_type == 'Aufgabe':
                resultdict = validation.formatoutputs(result)
                resultdict = validation.formataufgabe(resultdict)
                if resultdict['again'] == True:
                    again = True
            elif obj.portal_type == 'Experiment':
                formkeys = result.keys()
                formkeys.sort()
                resultdict = validation.formatoutputs(formkeys, result)
                resultdict = validation.formatexperiment(resultdict)
                if resultdict['again'] == True:
                    again = True
            resultdict['type'] = obj.portal_type
            resultdict['name'] = i
            contentlist.append(resultdict)
            contentdir.append((self.context.absolute_url()+'/@@arbeitsblattplone/#'+i, obj.Title()))
        retdict['contentlist'] = contentlist
        retdict['contentdir'] = contentdir
        portal = ploneapi.portal.get().absolute_url()
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['questionurl'] = self.context.absolute_url() + '/@@arbeitsblattplone'
        retdict['again'] = again
        retdict['art'] = self.context.art
        if self.context.art == 'benotet':
            cookie = self.cookiesetter(retdict)
        return retdict

class ArbeitsblattView(api.Page):
    api.context(IArbeitsblatt)

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
        self.datei = {}
        if self.context.datei:
            self.datei['url'] = "%s/@@download/datei/%s" %(self.context.absolute_url(), self.context.datei.filename)
            self.datei['contentType'] = self.context.datei.contentType
            self.datei['size'] = sizeof_fmt(self.context.datei.size)
            self.datei['filename'] = self.context.datei.filename


