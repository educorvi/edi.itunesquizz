from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from edi.itunesquizz.experiment import IExperiment
from edi.itunesquizz.experiment import aufgabenart, ergebnisart
from edi.itunesquizz.browser.security import checkOwner

api.templatedir('templates')

def myfloat(value):
    value = value.replace(',', '.')
    return float(value)

class ExperimentITunes(api.View):
    api.context(IExperiment)

    def formatinputs(self):
        reihen = []
        if self.context.versuchsreihen:
            for i in self.context.versuchsreihen:
                reihe = {}
                if i.get('antwort'):
                    reihe['label'] = i.get('antwort')
                    reihe['value'] = 'reihe_%s_%s' %(self.context.UID(), self.context.versuchsreihen.index(i))
                    reihe['einheit'] = i.get('einheit')
                    reihen.append(reihe)
        return reihen
               
    def update(self):
        retdict = {}
        portal = ploneapi.portal.get().absolute_url()
        retdict['title'] = self.context.title
        retdict['aufgabe'] = self.context.aufgabe
        retdict['punkte'] = self.context.punkte
        retdict['validationurl'] = self.context.absolute_url() + '/@@validateexperiment'
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        illustration = ''
        if self.context.image:
            retdict['illustration'] = 'bild'
            retdict['bild'] = '%s/@@images/image' % self.context.absolute_url()
        if self.context.video:
            retdict['illustration'] = 'film'
            retdict['film'] = self.context.video
        retdict['fieldname'] = self.context.id
        retdict['inputfields'] = self.formatinputs()
        retdict['fazit'] = self.context.fazit
        return retdict


class ValidateExperiment(api.View):
    api.context(IExperiment)

    def formatoutputs(self, formkeys, test):
        resultdict = {}
        results = []
        again = False
        result = True
        versuchsreihen=self.context.versuchsreihen
        for i in range(len(versuchsreihen)):
            reihe = versuchsreihen[i]
            erwartung = reihe.get('erwartung')
            ergebnis = reihe.get('ergebnis')
            experiment = test.get(formkeys[i])
            myresult = {}
            if erwartung == 'integer':
                if int(experiment) != int(ergebnis):
                    again = True
                    result = False
            if erwartung == 'float':
                if myfloat(experiment) != myfloat(ergebnis):
                    again = True
                    result = False
            if erwartung == 'intrange':
                ergebnis = ergebnis.split('|')
                if not int(ergebnis[0]) < int(experiment) < int(ergebnis[1]):
                    again = True
                    result = False
            if erwartung == 'floatrange':
                ergebnis = ergebnis.split('|')
                if not myfloat(ergebnis[0]) < myfloat(experiment) < myfloat(ergebnis[1]):
                    again = True
                    result = False
            myresult['label'] = reihe.get('antwort')
            myresult['experiment'] = experiment
            myresult['einheit'] = reihe.get('einheit')
            results.append(myresult)
        resultdict['again'] = again
        resultdict['result'] = result
        resultdict['results'] = results
        resultdict['fazit'] = test.get('fazit')
        return resultdict

    def formatexperiment(self, retdict):
        retdict['title'] = self.context.title
        retdict['aufgabe'] = self.context.aufgabe
        retdict['art'] = self.context.art
        retdict['erklaerung'] = self.context.erklaerung
        return retdict

    def cookiesetter(self, retdict):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("qrdata", retdict)

    def update(self):
        retdict = {}
        questionurl = self.context.absolute_url() + '/@@experimentitunes'
        formkeys = []
        for i in self.request.form.keys():
            if i .startswith('reihe'):
                formkeys.append(i)
        if not formkeys:
            return self.response.redirect(questionurl)
        retdict['questionurl'] = questionurl
        portal = ploneapi.portal.get().absolute_url()
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict = self.formatexperiment(retdict)
        formkeys.sort()
        test = self.request.form
        outputs = self.formatoutputs(formkeys, test)
        retdict['outputs'] = outputs
        if self.context.art == 'benotet':
            cookie = self.cookiesetter(retdict)
        return retdict


class ExperimentView(api.Page):
    api.context(IExperiment)

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
        self.aufgabenart = aufgabenart.getTerm(self.context.art).title
        self.images = False
        if self.context.webcode:
            self.ituneslink = portal + '/@@itunesview?code=' + self.context.webcode
        else:
            self.ituneslink = self.context.absolute_url() + '/@@experimentitunes'
        self.versuchsreihen = []
        if self.context.versuchsreihen:
            for i in self.context.versuchsreihen:
                entry = {}
                entry['antwort'] = i.get('antwort')
                entry['erwartung'] = ergebnisart.getTerm(i.get('erwartung')).title
                entry['ergebnis'] = i.get('ergebnis').replace('|', ' bis ')
                entry['einheit'] = i.get('einheit')
                self.versuchsreihen.append(entry)
