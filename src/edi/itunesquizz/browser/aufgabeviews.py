# -*- coding: utf-8 -*-
from zope.interface import Interface
from plone import api as ploneapi
from edi.itunesquizz.aufgabe import IAufgabe
from edi.itunesquizz.aufgabe import aufgabenart
from edi.itunesquizz.browser.security import checkOwner
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
try:
    from edi.course.persistance import getResultsForQuiz
except:
    getResultsForQuiz = None
from Products.Five import BrowserView

timersnippet = """\
<script>
  var timeleft = %s;
  var downloadTimer = setInterval(function(){
  document.getElementById("progressBar").value = %s - timeleft;
  timeleft -= 1;
  if(timeleft <= 0)
  clearInterval(downloadTimer);
  }, 1000);
</script>"""

delaysnippet = """\
<script>
  setTimeout("location.href = '%s/%s';",%s);
</script>"""


def sizeof_fmt(num, suffix='Byte'):
    for unit in ['','k','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)

def backcolor(bewertung):
    colors = {'richtig':'list-group-item list-group-item-success',
              'falsch':'list-group-item list-group-item-danger'}
    return colors.get(bewertung)

class AufgabeITunes(BrowserView):

    def formatinputs(self):
        options = []
        if self.context.antworten:
            for i in self.context.antworten:
                option = {}
                if i.get('antwort'):
                    option['image'] = ''
                    if i.get('image'):
                        imgobj = ploneapi.content.get(UID = i.get('image'))
                        option['image'] = '%s/@@images/image/preview' % imgobj.absolute_url()
                    option['value'] = 'option_%s' %self.context.antworten.index(i)
                    option['label'] = i.get('antwort')
                    options.append(option)
        return options

    def set_bedenkzeit(self):
        self.timersnippet = timersnippet %(self.context.bedenkzeit, self.context.bedenkzeit)
        self.delaysnippet = delaysnippet %(self.context.absolute_url(), '@@validateaufgabe', self.context.bedenkzeit * 1000)

    def check_edicourse(self):
        return

    def get_validationurl(self):
        return self.context.absolute_url() + '/@@validateaufgabe'
               
    def update(self):
        self.check_edicourse()
        retdict = {}
        portal = ploneapi.portal.get().absolute_url()
        self.statics= portal + '/++resource++edi.itunesquizz'
        portal = ploneapi.portal.get().absolute_url()
        retdict['validationurl'] = self.get_validationurl()
        retdict['statics'] = portal + '/++resource++edi.itunesquizz'
        retdict['title'] = self.context.title
        retdict['aufgabe'] = self.context.aufgabe
        retdict['punkte'] = self.context.punkte
        if self.context.hinweis:
            retdict['hinweis'] = self.context.hinweis.output
        else:
            retdict['hinweis'] = ''
        retdict['bild'] = ''
        retdict['datei'] = {}
        if self.context.datei:
            datei = {}
            datei['url'] = "%s/@@filedownload" % self.context.absolute_url()
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
            retdict['bild'] = '%s/@@images/image/large' % self.context.absolute_url()
        if self.context.video:
            illustration = 'film'
            retdict['film'] = self.context.video
        retdict['bedenkzeit'] = self.context.bedenkzeit
        if self.context.bedenkzeit > 0:
            self.set_bedenkzeit()
        retdict['illustration'] = illustration
        retdict['fieldname'] = self.context.id
        retdict['inputfields'] = self.formatinputs()
        return retdict

class AufgabePlone(AufgabeITunes):

    def set_bedenkzeit(self):
        self.timersnippet = timersnippet %(self.context.bedenkzeit, self.context.bedenkzeit)
        self.delaysnippet = delaysnippet %(self.context.absolute_url(), '@@validateaufgabeplone', self.context.bedenkzeit * 1000)

    def check_edicourse(self):
        registry = getUtility(IRegistry)
        if registry['edi.itunesquizz.settings.IQuizSettings.iscoursesite'] and getResultsForQuiz:
            retdict = getResultsForQuiz(self.context)
            if retdict:
                returl = self.context.absolute_url() + '/@@validateaufgabeplone'
                self.request.response.redirect(returl)

    def get_validationurl(self):
        return self.context.absolute_url() + '/@@validateaufgabeplone'

class AufgabeVue(AufgabePlone):
    """Rendert ein Javascript"""

class ValidateAufgabe(BrowserView):

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
                myresult['bewertung'] = backcolor(i.get('bewertung'))
                resultoption = 'option_%s' %self.context.antworten.index(i)
                if not test:
                    myresult['checkbox'] = 'glyphicon glyphicon-unchecked'
                    myresult['checkbox-img'] = 'glyphicons-halflings-59-square-empty.svg'
                    result = False
                    again = True
                else:
                    if resultoption in test:
                        myresult['checkbox'] = 'glyphicon glyphicon-check'
                        myresult['checkbox-img'] = 'glyphicons-halflings-76-square-checkbox.svg'
                        if i.get('bewertung') == u'falsch':
                            result = False
                            again = True
                    else:
                        myresult['checkbox'] = 'glyphicon glyphicon-unchecked'
                        myresult['checkbox-img'] = 'glyphicons-halflings-59-square-empty.svg'
                        if i.get('bewertung') == u'richtig':
                            result = False
                            again = True
                results.append(myresult)
        resultdict['again'] = again
        resultdict['result'] = result
        resultdict['results'] = results
        return resultdict

    def get_overrideemojis(self):
        registry = getUtility(IRegistry)
        override_emojis = {'true_emoji':'', 'false_emoji':''}
        override_true = registry['edi.itunesquizz.settings.IQuizSettings.true_emoji']
        if override_true:
            try:
               emoji_obj = ploneapi.content.get(UID = override_true)
               override_emojis['true_emoji'] = "%s/@@images/image/tile" %emoji_obj.absolute_url()
            except:
               pass # Default Emoji
        override_false = registry['edi.itunesquizz.settings.IQuizSettings.false_emoji']
        if override_false:
            try:
               emoji_obj = ploneapi.content.get(UID = override_false)
               override_emojis['false_emoji'] = "%s/@@images/image/tile" %emoji_obj.absolute_url()
            except:
               pass # Default Emoji
        return override_emojis

    def get_overridecomments(self):
        registry = getUtility(IRegistry)
        override_comments = {'true_comment':u'Prima, das war richtig!', 'false_comment':u'Hm..., das war leider falsch!'}
        override_true = registry['edi.itunesquizz.settings.IQuizSettings.true_comment']
        if override_true:
            override_comments['true_comment'] = override_true
        override_false = registry['edi.itunesquizz.settings.IQuizSettings.false_comment']
        if override_false:
            override_comments['false_comment'] = override_false
        return override_comments

    def formataufgabe(self, retdict):
        registry = getUtility(IRegistry)
        retdict['emoji'] = True
        if not registry['edi.itunesquizz.settings.IQuizSettings.emoji']:
           retdict['emoji'] = False
        retdict['qrcode'] = registry['edi.itunesquizz.settings.IQuizSettings.qrcode']
        override_emojis = self.get_overrideemojis()
        retdict['true_emoji'] = override_emojis.get('true_emoji')
        retdict['false_emoji'] = override_emojis.get('false_emoji')
        comments = self.get_overridecomments()
        retdict['true_comment'] = comments.get('true_comment')
        retdict['false_comment'] = comments.get('false_comment')
        retdict['title'] = self.context.title
        retdict['aufgabe'] = self.context.aufgabe
        retdict['art'] = self.context.art
        retdict['punkte'] = self.context.punkte
        retdict['erklaerung'] = ''
        if self.context.erklaerung:
            retdict['erklaerung'] = self.context.erklaerung.output
        retdict['illustration'] = ''
        if self.context.solutionimage:
            retdict['illustration'] = 'bild'
        if self.context.solutionvideo:
            retdict['illustration'] = 'film'
        retdict['block-erklaerung'] = False
        if self.context.art == 'selbsttest':
            if retdict['erklaerung'] or retdict['illustration']:
                retdict['block-erklaerung'] = True
        retdict['bild'] = ''
        if self.context.solutionimage:
            retdict['bild'] = "%s/@@images/solutionimage/large" %self.context.absolute_url()
        retdict['film'] = ''
        if self.context.solutionvideo:
            retdict['film'] = self.context.solutionvideo
        return retdict

    def cookiesetter(self, retdict):
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        session.set("qrdata", retdict)

    def get_edicourse(self):
        return {}

    def get_questionurl(self):
        return self.context.absolute_url() + '/@@aufgabeitunes'
        
    def update(self):
        retdict = self.get_edicourse()
        questionurl = self.get_questionurl()
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


class ValidateAufgabePlone(ValidateAufgabe):

    def get_edicourse(self):
        retdict = {}
        registry = getUtility(IRegistry)
        if registry['edi.itunesquizz.settings.IQuizSettings.iscoursesite'] and getResultsForQuiz:
            retdict = getResultsForQuiz(self.context)
            if retdict:
                return retdict
        return retdict

    def get_questionurl(self):
        return self.context.absolute_url() + '/@@aufgabeplone'

class ValidateVue(BrowserView):

    def __call__(self):
        import pdb;pdb.set_trace()


class AufgabeView(BrowserView):

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
        registry = getUtility(IRegistry)
        self.isquizsite = registry['edi.itunesquizz.settings.IQuizSettings.isquizsite']
        self.kursordner = self.context.aq_parent.absolute_url()
        portal = ploneapi.portal.get().absolute_url()
        self.statics = portal + '/++resource++edi.itunesquizz'
        self.datei = {}
        if self.context.datei:
            self.datei['url'] = "%s/@@filedownload" % self.context.absolute_url()
            self.datei['contentType'] = self.context.datei.contentType
            self.datei['size'] = sizeof_fmt(self.context.datei.size)
            self.datei['filename'] = self.context.datei.filename
        self.aufgabenart = aufgabenart.getTerm(self.context.art).title
        self.video = ''
        if self.context.video:
            self.video = self.context.video
        self.images = False
        if hasattr(self.context, 'webcode'):
            if self.context.webcode:
                self.ituneslink = portal + '/@@itunesview?code=' + self.context.webcode
        else:
            self.ituneslink = self.context.absolute_url() + '/@@aufgabeitunes'
        self.messagelink = self.context.absolute_url() + '/@@messenger'
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
        self.bedenkzeit = ''
        if self.context.bedenkzeit > 0:
            self.bedenkzeit = u"Für diese Aufgabe wurde eine Bedenkzeit von %s Sekunden eingestellt." %self.context.bedenkzeit
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
