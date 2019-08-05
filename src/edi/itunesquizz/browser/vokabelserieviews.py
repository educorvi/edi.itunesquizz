from zope.interface import Interface
from plone import api as ploneapi
from edi.itunesquizz.vokabelserie import IVokabelserie
from edi.itunesquizz.browser.security import checkOwner
from Products.Five import BrowserView

def sizeof_fmt(num, suffix='Byte'):
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)


class VokabelserieITunes(BrowserView):

    def wizard(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        wiz = session.get("wizard", [])
        return len(wiz)

    def checkstartseite(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        start = session.get("startseite", 1)
        return start
        
    def update(self):
        myobjindex = self.wizard()
        retdict = {}
        portal = ploneapi.portal.get().absolute_url()
        retdict['validationurl'] = self.context.absolute_url() + '/@@validatevokabelserie'
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        if myobjindex == 0 and self.checkstartseite() == 1:
            retdict['start'] = True
            retdict['text'] = self.context.textvor.output
            retdict['validationurl'] = self.context.absolute_url() + '/@@checkstartseite'
            return retdict
        parts = self.context.parts
        if myobjindex == len(parts):
            url = self.context.absolute_url() + '/@@vokabelseriefinal'
            return self.request.response.redirect(url)
        myobjuid = parts[myobjindex]
        myobj = ploneapi.content.get(UID=myobjuid)
        retdict['start'] = False
        retdict['aufforderung'] = myobj.aufforderung
        retdict['aufgabe'] = myobj.aufgabe
        retdict['punkte'] = myobj.punkte
        retdict['datei'] = {}
        if myobj.dateiaufgabe:
            datei = {}
            datei['url'] = "%s/@@download/dateiaufgabe/%s" %(myobj.absolute_url(), myobj.dateiaufgabe.filename)
            if myobj.dateiaufgabe.contentType.startswith('audio'):
                datei['contentType'] = 'audio/mpeg'
            else:
                datei['contentType'] = myobj.dateiaufgabe.contentType
            datei['size'] = sizeof_fmt(myobj.dateiaufgabe.size)
            datei['filename'] = myobj.dateiaufgabe.filename
            retdict['datei'] = datei
        retdict['uid'] = myobj.UID()
        retdict['fieldname'] = myobj.id
        retdict['bedenkzeit'] = myobj.bedenkzeit
        if myobj.bedenkzeit > 0:
            self.timersnippet = """\
              <script>
                var timeleft = %s;
                var downloadTimer = setInterval(function(){
                document.getElementById("progressBar").value = %s - timeleft;
                timeleft -= 1;
                if(timeleft <= 0)
                clearInterval(downloadTimer);
                }, 1000);
              </script>""" %(myobj.bedenkzeit, myobj.bedenkzeit)
            self.delaysnippet = """\
              <script>
                setTimeout("location.href = '@@validatevokabelserie';",%s);
              </script>""" %(myobj.bedenkzeit * 1000)
        retdict['speakbutton'] = ''
        if myobj.sprecher:
            retdict['speakbutton'] = "responsiveVoice.speak('%s','%s');" %(myobj.aufgabe, myobj.sprecher)
        return retdict


class CheckStartSeite(BrowserView):

    def __call__(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        start = session.get("startseite", 1)
        session.set("startseite", 2)
        url = self.context.absolute_url() + '/@@vokabelserieitunes'
        return self.request.response.redirect(url)


class VokabelseriePlone(BrowserView):

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


class ValidateVokabelserie(BrowserView):

    def wizard(self, current):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        wiz = session.get("wizard", [])
        if current not in wiz:
            wiz.append(current)
            session.set("wizard", wiz)

    def next(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        wiz = session.get("wizard", [])
        parts = self.context.parts
        if parts:
            next = parts[len(wiz)]
            return next
        return None

    def cookiesetter(self, retdict):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        results = session.get("qrdata", [])
        if retdict not in results:
            results.append(retdict)
        session.set("qrdata", results)

    def formatoutputs(self, currentobj, test):
        resultdict = {}
        again = True
        result = False
        eingabe = test
        if not currentobj.antwort:
            result = 'text'
        else:
            if currentobj.upper_lower:
                for i in currentobj.antwort:
                    if i == test.decode('utf-8'):
                        result = True
                        again = False
            else:
                for i in currentobj.antwort:
                    if i.lower() == test.decode('utf-8').lower():
                        result = True
                        again = False
        resultdict['again'] = again
        resultdict['result'] = result
        resultdict['eingabe'] = eingabe
        return resultdict

    def formatvocabeltest(self, retdict, currentobj):
        retdict['title'] = currentobj.title
        retdict['aufforderung'] = currentobj.aufforderung
        retdict['aufgabe'] = currentobj.aufgabe
        retdict['art'] = currentobj.art
        retdict['datei'] = {}
        if currentobj.dateiaufgabe:
            retdict['datei']['url'] = "%s/@@download/dateiaufgabe/%s" %(currentobj.absolute_url(), currentobj.dateiaufgabe.filename)
            if currentobj.dateiaufgabe.contentType.startswith('audio'):
                retdict['datei']['contentType'] = 'audio/mpeg'
            else:
                retdict['datei']['contentType'] = currentobj.dateiaufgabe.contentType
            retdict['datei']['size'] = sizeof_fmt(currentobj.dateiaufgabe.size)
            retdict['datei']['filename'] = currentobj.dateiaufgabe.filename
        return retdict

    def update(self):
        current = self.request.get('current')
        savecurrent = self.wizard(current)
        currentobj = ploneapi.content.get(UID=current)
        retdict = {}
        nexturl = self.context.absolute_url() + '/@@vokabelserieitunes'
        portal = ploneapi.portal.get().absolute_url()
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['nexturl'] = nexturl
        retdict = self.formatvocabeltest(retdict, currentobj)
        outputs = {}
        fieldname = currentobj.id
        if self.request.form.get(fieldname):
            outputs = self.formatoutputs(currentobj, self.request.form.get(fieldname))
        else:
            outputs['again'] = True
            outputs['result'] = False
            outputs['eingabe'] = ''
        retdict['outputs'] = outputs
        cookie = self.cookiesetter(retdict)
        return retdict

class VokabelserieFinal(BrowserView):

    def update(self):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        results = session.get("qrdata", [])
        retdict = {}
        portal = ploneapi.portal.get().absolute_url()
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['title'] = self.context.title
        retdict['text'] = self.context.textnach.output
        retdict['outputs'] = results
        return retdict
            
class ValidateVokabelseriePlone(BrowserView):

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

class VokabelserieView(BrowserView):

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
