from datetime import datetime
import qrcode
import numpy as np
import requests
from PIL import Image
from zope.interface import Interface
from cStringIO import StringIO
from uvc.api import api
from plone import api as ploneapi
from pymongo import MongoClient

class QRImage(api.View):
    api.context(Interface)

    def render(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
            )
        client = MongoClient('localhost', 27017)
        db = client.itunesu
        collection = db.quizzes
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        aufgabedata = session.get('qrdata')
        now = datetime.now()
        aufgabedata['_id'] = '%s%s%s%s%s%s%s' %(now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond) 
        myid = collection.insert_one(aufgabedata).inserted_id
        valtype = self.context.portal_type.lower()
        url = "%s/@@itunes_%s_validation?id=%s" %(self.context.absolute_url(), valtype, str(myid))
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()

        output = StringIO()
        img.save(output)
        filename = self.context.id + '.png'

        if self.context.bonus:
            qrimage = Image.open(StringIO(output.getvalue()))
            url = "%s/@@download/bonus" % self.context.absolute_url()

            response = requests.get(url)
            logoimage = Image.open(StringIO(response.content))
            quotient = float(logoimage.width) / float(logoimage.height)
            faktor = qrimage.width
            new_width = quotient * faktor
            newlogo = logoimage.resize((int(new_width), faktor), Image.ANTIALIAS)
            
            newsize = (newlogo.size[0] + faktor, newlogo.size[1])       

            montage = Image.new(mode='RGBA', size=newsize, color=(55,55,55,55))
            montage.paste(newlogo, (0,0))
            montage.paste(qrimage, (newlogo.size[0], 0))


            montage.save('/tmp/%s' %filename)
            myfile = open('/tmp/%s' %filename, 'r')
            myfile.seek(0)

            self.request.response.setHeader('Content-Type', 'image/png')
            self.request.response.setHeader('filename', filename)
            return myfile.read()

        self.request.response.setHeader('Content-Type', 'image/png')
        self.request.response.setHeader('filename', filename)
        return output.getvalue()


class QRDownload(api.View):
    api.context(Interface)

    def render(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
            )
        qr.add_data(self.context.UID())
        qr.make(fit=True)
        img = qr.make_image()

        output = StringIO()
        img.save(output)
        qrimage = Image.open(StringIO(output.getvalue()))

        #response = requests.get('https://itunesu.educorvi.de/@@site-logo/educorvi_orange_300.png')
        #response = requests.get('https://itunesu.educorvi.de/Members/lars--walther--1/deh-dmz-zdk/kraeks_uebung.png')
        response = requests.get('https://itunesu.educorvi.de/Members/lars--walther--1/deh-dmz-zdk/kraeks_410.png')
        logoimage = Image.open(StringIO(response.content))

        montage = Image.new(mode='RGBA', size=(410, 660), color=(55,55,55,55))
        montage.paste(logoimage, (0,0)) 
        montage.paste(qrimage, (0,250))

        montage.save('/tmp/newimg.png')
        myfile = open('/tmp/newimg.png', 'r')
        myfile.seek(0)

        self.request.response.setHeader('Content-Type', 'image/png')
        self.request.response.setHeader('filename', 'meintest.png')
        return myfile.read()
