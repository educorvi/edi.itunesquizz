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
        retdict = {}
        portal = ploneapi.portal.get().absolute_url()
        retdict['validationurl'] = self.context.absolute_url() + '/@@validateaufgabe'
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['title'] = self.context.title
        retdict['aufgabe'] = self.context.aufgabe
        retdict['punkte'] = self.context.punkte
        retdict['hinweis'] = self.context.hinweis
        illustration = ''
        if self.context.image:
            illustration = 'bild'
            retdict['bild'] = '%s/@@images/image' % self.context.absolute_url()
        if self.context.video:
            illustration = 'film'
            retdict['film'] = self.context.absolute_url()
        retdict['illustration'] = illustration
        retdict['fieldname'] = self.context.id
        retdict['inputfields'] = self.formatinputs()
        return retdict

class ValidateAufgabe(api.View):
    api.context(IAufgabe)

    def formatoutputs(self, test):
        resultdict = {}
        results = []
        again = False
        result = True
        if not self.context.antworten:
            result = 'text'
            results = test
        for i in self.context.antworten:
            myresult = {}
            if i.get('antwort'):
                myresult['label'] = i.get('antwort')
                resultoption = 'option_%s' %self.context.antworten.index(i)
                if not test:
                    myresult['checkbox'] = 'glyphicon glyphicon-unchecked'
                    result = False
                    again = True
                else:
                    if resultoption in test:
                        myresult['checkbox'] = 'glyphicon glyphicon-check'
                        if i.get('bewertung') == u'falsch':
                            result = False
                            again = True
                    else:
                        myresult['checkbox'] = 'glyphicon glyphicon-unchecked'
                        if i.get('bewertung') == u'richtig':
                            result = False
                            again = True
                results.append(myresult)
        resultdict['again'] = again
        resultdict['result'] = result
        resultdict['results'] = results
        return resultdict

    def formataufgabe(self, retdict):
        retdict['title'] = self.context.title
        retdict['aufgabe'] = self.context.aufgabe
        retdict['art'] = self.context.art
        retdict['erklaerung'] = self.context.erklaerung
        retdict['illustration'] = ''
        if self.context.solutionimage:
            retdict['illustration'] = 'bild'
        if self.context.solutionvideo:
            retdict['illustration'] = 'film'
        retdict['bild'] = ''
        if self.context.solutionimage:
            retdict['bild'] = "%s/@@images/solutionimage" %self.context.absolute_url()
        retdict['film'] = ''
        if self.context.solutionvideo:
            retdict['film'] = self.context.solutionvideo
        return retdict

    def cookiesetter(self, retdict):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("qrdata", retdict)
        
    def update(self):
        retdict = {}
        questionurl = self.context.absolute_url() + '/@@aufgabeitunes'
        if not self.request.form.get(self.context.id):
            return self.response.redirect(questionurl)
        portal = ploneapi.portal.get().absolute_url()
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['questionurl'] = questionurl
        retdict = self.formataufgabe(retdict)
        outputs = {}
        fieldname = self.context.id
        outputs = self.formatoutputs(self.request.form.get(fieldname))
        retdict['outputs'] = outputs
        if self.context.art == 'benotet':
            cookie = self.cookiesetter(retdict)
        return retdict

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
        self.solutionimage = ''
        if self.context.solutionimage:
            self.solutionimage = "%s/@@images/solutionimage" %self.context.absolute_url()
        self.solutionvideo = ''
        if self.context.solutionvideo:
            self.solutionvideo = self.context.solutionvideo
        self.bonus = ''
        if self.context.bonus:
            self.bonus = "%s/@@images/bonus" %self.context.absolute_url()
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
