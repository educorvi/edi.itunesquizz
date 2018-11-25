from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from edi.itunesquizz.experiment import IExperiment
from edi.itunesquizz.experiment import ergebnisart

api.templatedir('templates')


class ExperimentITunes(api.View):
    api.context(IExperiment)

    def formatinputs(self):
        reihen = []
        if self.context.versuchsreihen:
            for i in self.context.versuchsreihen:
                reihe = {}
                if i.get('antwort'):
                    reihe['label'] = i.get('antwort')
                    reihe['value'] = 'reihe_%s' %self.context.antworten.index(i)
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

    def formatoutputs(self):
        results = []
        self.again = False
        self.result = True
        fieldname = self.context.id
        test = self.request.form.get(fieldname)
        for i in self.context.antworten:
            result = {}
            if i.get('antwort'):
                result['label'] = i.get('antwort')
                resultoption = 'option_%s' %self.context.antworten.index(i)
                if resultoption in test:
                    result['checkbox'] = 'glyphicon glyphicon-check'
                    if i.get('bewertung') == u'falsch':
                        self.result = False
                        self.again = True
                else:
                    result['checkbox'] = 'glyphicon glyphicon-unchecked'
                    if i.get('bewertung') == u'richtig':
                        self.result = False
                        self.again = True
                results.append(result)
        return results

    def update(self):
        self.questionurl = self.context.absolute_url() + '/@@experimentitunes'
        if not self.request.form.get(self.context.id):
            return self.response.redirect(self.questionurl)
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.illustration = ''
        if self.context.solutionimage:
            self.illustration = 'bild'
        if self.context.solutionvideo:
            self.illustration = 'film'
        self.outputfields = []
        if self.context.art == u'selbsttest':
            self.outputfields = self.formatoutputs()


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
                entry['ergebnis'] = i.get('ergebnis')
                self.versuchsreihen.append(entry)
