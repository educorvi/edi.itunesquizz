from zope.interface import Interface
from plone import api as ploneapi
from edi.itunesquizz.vokabeltest import IVokabeltest
from edi.itunesquizz.vokabeltest import aufgabenart
from edi.itunesquizz.browser.security import checkOwner
from Products.Five import BrowserView

def sizeof_fmt(num, suffix='Byte'):
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)


class VokabeltestITunes(BrowserView):

    def update(self):
        retdict = {}
        portal = ploneapi.portal.get().absolute_url()
        retdict['validationurl'] = self.context.absolute_url() + '/@@validatevokabeltest'
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['aufforderung'] = self.context.aufforderung
        retdict['aufgabe'] = self.context.aufgabe
        retdict['punkte'] = self.context.punkte
        retdict['datei'] = {}
        if self.context.dateiaufgabe:
            datei = {}
            datei['url'] = "%s/@@download/dateiaufgabe/%s" %(self.context.absolute_url(), self.context.dateiaufgabe.filename)
            if self.context.dateiaufgabe.contentType.startswith('audio'):
                datei['contentType'] = 'audio/mpeg'
            else:
                datei['contentType'] = self.context.dateiaufgabe.contentType
            datei['size'] = sizeof_fmt(self.context.dateiaufgabe.size)
            datei['filename'] = self.context.dateiaufgabe.filename
            retdict['datei'] = datei
        retdict['fieldname'] = self.context.id
        retdict['bedenkzeit'] = self.context.bedenkzeit
        if self.context.bedenkzeit > 0:
            self.timersnippet = """\
              <script>
                var timeleft = %s;
                var downloadTimer = setInterval(function(){
                document.getElementById("progressBar").value = %s - timeleft;
                timeleft -= 1;
                if(timeleft <= 0)
                clearInterval(downloadTimer);
                }, 1000);
              </script>""" %(self.context.bedenkzeit, self.context.bedenkzeit)
            self.delaysnippet = """\
              <script>
                setTimeout("location.href = '@@validatevokabeltest';",%s);
              </script>""" %(self.context.bedenkzeit * 1000)
        retdict['speakbutton'] = ''
        if self.context.sprecher:
            retdict['speakbutton'] = "responsiveVoice.speak('%s','%s');" %(self.context.aufgabe, self.context.sprecher)
        return retdict


class VokabeltestPlone(BrowserView):

    def update(self):
        retdict = {}
        portal = ploneapi.portal.get().absolute_url()
        retdict['validationurl'] = self.context.absolute_url() + '/@@validatevokabeltest'
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['aufforderung'] = self.context.aufforderung
        retdict['aufgabe'] = self.context.aufgabe
        retdict['punkte'] = self.context.punkte
        retdict['datei'] = {}
        if self.context.dateiaufgabe:
            datei = {}
            datei['url'] = "%s/@@download/dateiaufgabe/%s" %(self.context.absolute_url(), self.context.dateiaufgabe.filename)
            if self.context.dateiaufgabe.contentType.startswith('audio'):
                datei['contentType'] = 'audio/mpeg'
            else:
                datei['contentType'] = self.context.dateiaufgabe.contentType
            datei['size'] = sizeof_fmt(self.context.dateiaufgabe.size)
            datei['filename'] = self.context.dateiaufgabe.filename
            retdict['datei'] = datei
        retdict['fieldname'] = self.context.id
        retdict['bedenkzeit'] = self.context.bedenkzeit
        if self.context.bedenkzeit > 0:
            self.timersnippet = """\
              <script>
                var timeleft = %s;
                var downloadTimer = setInterval(function(){
                document.getElementById("progressBar").value = %s - timeleft;
                timeleft -= 1;
                if(timeleft <= 0)
                clearInterval(downloadTimer);
                }, 1000);
              </script>""" %(self.context.bedenkzeit, self.context.bedenkzeit)
            self.delaysnippet = """\
              <script>
                setTimeout("location.href = '@@validatevokabeltest';",%s);
              </script>""" %(self.context.bedenkzeit * 1000)
        retdict['speakbutton'] = ''
        if self.context.sprecher:
            retdict['speakbutton'] = "responsiveVoice.speak('%s','%s');" %(self.context.aufgabe, self.context.sprecher)
        return retdict


class ValidateVokabeltest(BrowserView):

    def formatoutputs(self, test):
        resultdict = {}
        again = True
        result = False
        eingabe = test
        if not self.context.antwort:
            result = 'text'
        else:
            if self.context.upper_lower:
                for i in self.context.antwort:
                    if i == test.decode('utf-8'):
                        result = True
                        again = False
            else:
                for i in self.context.antwort:
                    if i.lower() == test.decode('utf-8').lower():
                        result = True
                        again = False
        resultdict['again'] = again
        resultdict['result'] = result
        resultdict['eingabe'] = eingabe
        return resultdict

    def formatvocabeltest(self, retdict):
        retdict['title'] = self.context.title
        retdict['aufforderung'] = self.context.aufforderung
        retdict['aufgabe'] = self.context.aufgabe
        retdict['art'] = self.context.art
        retdict['datei'] = {}
        if self.context.dateiaufgabe:
            retdict['datei']['url'] = "%s/@@download/dateiaufgabe/%s" %(self.context.absolute_url(), self.context.dateiaufgabe.filename)
            if self.context.dateiaufgabe.contentType.startswith('audio'):
                retdict['datei']['contentType'] = 'audio/mpeg'
            else:
                retdict['datei']['contentType'] = self.context.dateiaufgabe.contentType
            retdict['datei']['size'] = sizeof_fmt(self.context.dateiaufgabe.size)
            retdict['datei']['filename'] = self.context.dateiaufgabe.filename
        return retdict

    def cookiesetter(self, retdict):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("qrdata", retdict)
        
    def update(self):
        retdict = {}
        questionurl = self.context.absolute_url() + '/@@vokabeltestitunes'
        portal = ploneapi.portal.get().absolute_url()
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['questionurl'] = questionurl
        retdict = self.formatvocabeltest(retdict)
        outputs = {}
        fieldname = self.context.id
        if self.request.form.get(fieldname):
            outputs = self.formatoutputs(self.request.form.get(fieldname))
        else:
            outputs['again'] = True
            outputs['result'] = False
            outputs['eingabe'] = ''
        retdict['outputs'] = outputs
        if self.context.art == 'benotet':
            cookie = self.cookiesetter(retdict)
        return retdict


class ValidateVokabeltestPlone(BrowserView):

    def formatoutputs(self, test):
        resultdict = {}
        eingabe = ''
        again = False
        result = True
        eingabe = test
        if not self.context.antwort:
            result = 'text'
        else:
            if self.context.upper_lower:
                if self.context.antwort != test:
                    result = False
                    again = True
            else:
                if self.context.antwort.lower() != test.lower():
                    result = False
                    again = True
        resultdict['again'] = again
        resultdict['result'] = result
        resultdict['eingabe'] = eingabe
        return resultdict

    def formatvocabeltest(self, retdict):
        retdict['title'] = self.context.title
        retdict['aufgabe'] = self.context.aufgabe
        retdict['art'] = self.context.art

    def cookiesetter(self, retdict):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("qrdata", retdict)

    def update(self):
        retdict = {}
        questionurl = self.context.absolute_url() + '/@@vokabeltestitunes'
        portal = ploneapi.portal.get().absolute_url()
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['questionurl'] = questionurl
        retdict = self.formatvocabeltest(retdict)
        outputs = {}
        fieldname = self.context.id
        outputs = self.formatoutputs(self.request.form.get(fieldname))
        retdict['outputs'] = outputs
        if self.context.art == 'benotet':
            cookie = self.cookiesetter(retdict)
        return retdict


class VokabeltestView(BrowserView):

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
        self.datei = {}
        if self.context.dateiaufgabe:
            self.datei['url'] = "%s/@@download/dateiaufgabe/%s" %(self.context.absolute_url(), self.context.dateiaufgabe.filename)
            if self.context.dateiaufgabe.contentType.startswith('audio'):
                self.datei['contentType'] = 'audio/mpeg'
            else:
                self.datei['contentType'] = self.context.dateiaufgabe.contentType
            self.datei['size'] = sizeof_fmt(self.context.dateiaufgabe.size)
            self.datei['filename'] = self.context.dateiaufgabe.filename
        self.aufgabenart = aufgabenart.getTerm(self.context.art).title
        self.images = False
        if self.context.webcode:
            self.ituneslink = portal + '/@@itunesview?code=' + self.context.webcode
        else:
            self.ituneslink = self.context.absolute_url + '/@@vokabeltestitunes'
        self.antwort = self.context.antwort
        self.bedenkzeit = self.context.bedenkzeit
        uplow = 'ja'
        if not self.context.upper_lower:
            uplow = 'nein'
        self.upper_lower = uplow
        self.aufforderung = self.context.aufforderung
