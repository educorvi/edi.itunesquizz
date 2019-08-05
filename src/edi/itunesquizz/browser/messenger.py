# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone import api as ploneapi
from os import system

class MessengerView(BrowserView):

    def message(self):
        portal = ploneapi.portal.get().absolute_url()
        message = u'/home/educorvi/education/zinstance/bin/yowsup-cli demos -c /home/educorvi/education/zinstance/yowsup.config -s %s "%s"'
        nachricht = u'*Neues edi.quiz:* '
        #nachricht += u'%s ' % self.context.title.decode('utf-8')
        if hasattr(self.context, 'webcode'):
            if self.context.webcode:
                ituneslink = portal + '/@@itunesview?code=' + self.context.webcode
        else:
            ituneslink = self.context.absolute_url() + '/@@aufgabeitunes'
        nachricht += ituneslink
        nachricht += u' _(diese Nachricht bitte nicht beantworten)_'
        phones = []
        if hasattr(self.request, 'form'):
            if self.request.form.get('mobil'):
                mobil = self.request.form.get('mobil')
                mobil = mobil.strip()
                if mobil.startswith('0'):
                    mobil = mobil[1:]
                mobil = mobil.replace(' ', '')
                mobil = mobil.replace('-', '')
                mobil = '49%s' % mobil
                phones.append(mobil)
        else: 
            phones = ['491622600497','491623737150']
        for i in phones:
            whatsapp = message % (i, nachricht)
            senden = system(whatsapp)
        return {'telefone':phones, 'nachricht':nachricht}
