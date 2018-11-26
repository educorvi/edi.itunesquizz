from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from edi.itunesquizz.experiment import IExperiment
from edi.itunesquizz.experiment import aufgabenart, ergebnisart

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
                    reihe['value'] = 'reihe_%s' %self.context.versuchsreihen.index(i)
                    reihe['einheit'] = i.get('einheit')
                    reihen.append(reihe)
        return reihen
               
    def update(self):
        portal = ploneapi.portal.get().absolute_url()
        self.validationurl = self.context.absolute_url() + '/@@validateexperiment'
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.illustration = ''
        if self.context.image:
            self.illustration = 'bild'
        if self.context.video:
            self.illustration = 'film'
        self.fieldname = self.context.id
        self.inputfields = self.formatinputs()
        return


class ValidateExperiment(api.View):
    api.context(IExperiment)

    def formatoutputs(self, formkeys):
        results = []
        self.again = False
        self.result = True
        formkeys.sort()
        versuchsreihen=self.context.versuchsreihen
        for i in range(len(versuchsreihen)):
            reihe = versuchsreihen[i]
            erwartung = reihe.get('erwartung')
            ergebnis = reihe.get('ergebnis')
            experiment = self.request.form.get(formkeys[i])
            result = {}
            if erwartung == 'integer':
                if int(experiment) != int(ergebnis):
                    self.again = True
                    self.result = False
            if erwartung == 'float':
                if myfloat(experiment) != myfloat(ergebnis):
                    self.again = True
                    self.result = False
            if erwartung == 'intrange':
                ergebnis = ergebnis.split('|')
                if not int(ergebnis[0]) < int(experiment) < int(ergebnis[1]):
                    self.again = True
                    self.result = False
            if erwartung == 'floatrange':
                ergebnis = ergebnis.split('|')
                if not myfloat(ergebnis[0]) < myfloat(experiment) < myfloat(ergebnis[1]):
                    self.again = True
                    self.result = False
            result['label'] = reihe.get('antwort')
            result['experiment'] = experiment
            result['einheit'] = reihe.get('einheit')
            results.append(result)
        return results

    def update(self):
        self.questionurl = self.context.absolute_url() + '/@@experimentitunes'
        marker = False
        formkeys = []
        for i in self.request.form.keys():
            if i .startswith('reihe'):
                formkeys.append(i)
        if not formkeys:
            return self.response.redirect(self.questionurl)
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.illustration = ''
        ##if self.context.solutionimage:
        #    self.illustration = 'bild'
        #if self.context.solutionvideo:
        #    self.illustration = 'film'
        self.outputfields = []
        if self.context.art == u'selbsttest':
            self.outputfields = self.formatoutputs(formkeys)


class ExperimentView(api.Page):
    api.context(IExperiment)

    def update(self):
        self.kursordner = self.context.aq_parent.absolute_url()
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.aufgabenart = aufgabenart.getTerm(self.context.art).title
        self.images = False
        if self.context.webcode:
            self.ituneslink = portal + '/@@itunesview?code=' + self.context.webcode
        else:
            self.ituneslink = self.context.absolute_url + '/@@experimentitunes'
        self.versuchsreihen = []
        if self.context.versuchsreihen:
            for i in self.context.versuchsreihen:
                entry = {}
                entry['antwort'] = i.get('antwort')
                entry['erwartung'] = ergebnisart.getTerm(i.get('erwartung')).title
                entry['ergebnis'] = i.get('ergebnis').replace('|', ' bis ')
                entry['einheit'] = i.get('einheit')
                self.versuchsreihen.append(entry)
