from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from edi.itunesquizz.aufgabe import IAufgabe
from edi.itunesquizz.aufgabe import aufgabenart

api.templatedir('templates')


class AufgabeITunes(api.View):
    api.context(IAufgabe)

    def formatinputs(self):
        options = []
        if self.context.antworten:
            for i in self.context.antworten:
                option = {}
                if i.get('antwort'):
                    option['image'] = ''
                    if i.get('image'):
                        parenturl = self.context.aq_parent.absolute_url()
                        option['image'] = '%s/%s/@@images/image' %(parenturl, i.get('image').id)
                    option['value'] = 'option_%s' %self.context.antworten.index(i)
                    option['label'] = i.get('antwort')
                    options.append(option)
        return options
               
    def update(self):
        portal = ploneapi.portal.get().absolute_url()
        self.validationurl = self.context.absolute_url() + '/@@validateaufgabe'
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.fieldname = self.context.id
        self.inputfields = self.formatinputs()
        return


class ValidateAufgabe(api.View):
    api.context(IAufgabe)

    def formatoutputs(self):
        results = []
        self.again = False
        fieldname = self.context.id
        test = self.request.form.get(fieldname)
        for i in self.context.antworten:
            result = {}
            if i.get('antwort'):
                result['label'] = i.get('antwort')
                resultoption = 'option_%s' %self.context.antworten.index(i)
                if resultoption in test:
                    result['checkbox'] = 'glyphicon glyphicon-check'
                    if i.get('bewertung') == u'richtig':
                        result['class'] = 'glyphicon glyphicon-ok'
                        result['style'] = 'color:green;'
                    else:
                        result['class'] = 'glyphicon glyphicon-remove'
                        result['style'] = 'color:red;'
                        self.again = True
                else:
                    result['checkbox'] = 'glyphicon glyphicon-unchecked'
                    if i.get('bewertung') == u'falsch':
                        result['class'] = 'glyphicon glyphicon-ok'
                        result['style'] = 'color:green;'
                    else:
                        result['class'] = 'glyphicon glyphicon-remove'
                        result['style'] = 'color:red;'
                        self.again = True
                results.append(result)
        return results

    def update(self):
        self.questionurl = self.context.absolute_url() + '/@@aufgabeitunes'
        if not self.request.form.get(self.context.id):
            return self.response.redirect(self.questionurl)
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.outputfields = []
        if self.context.art == u'selbsttest':
            self.outputfields = self.formatoutputs()


class AufgabeView(api.Page):
    api.context(IAufgabe)

    def update(self):
        self.kursordner = self.context.aq_parent.absolute_url()
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.aufgabenart = aufgabenart.getTerm(self.context.art).title
        self.images = False
        if self.context.webcode:
            self.ituneslink = portal + '/@@itunesview?code=' + self.context.webcode
        else:
            self.ituneslink = self.context.absolute_url + '/@@aufgabeitunes'
        self.antworten = []
        if self.context.antworten:
            for i in self.context.antworten:
                entry = {}
                entry['antwort'] = i.get('antwort')
                entry['bewertung'] = i.get('bewertung')
                entry['image'] = ''
                if i.get('image'):
                    self.images = True
                    image = ploneapi.content.find(UID = i.get('image'))[0].getObject()
                    entry['image'] = '%s/@@images/image/thumb' % image.absolute_url()
                self.antworten.append(entry)
