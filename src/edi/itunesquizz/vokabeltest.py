# -*- coding: utf-8 -*-
from zope.interface import Interface
from plone.dexterity.content import Item
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from z3c.form import field
from z3c.form import form
from z3c.form.form import extends
from zope import interface
from zope import component
from zope import schema
from plone.dexterity.browser import edit
from plone.dexterity.browser import add
from plone.supermodel import model
#from plone.directives import form
from plone.autoform import directives as form
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.field import NamedBlobFile
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.contenttypes.interfaces import IImage
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName
from zope.interface import invariant, Invalid
from zope.interface import directlyProvides
from z3c.form.browser.radio import RadioWidget
from plone.supermodel import model

wertvalues = SimpleVocabulary(
    [SimpleTerm(value=u'auswahl', token=u'auswahl', title=u'bitte auswählen'),
     SimpleTerm(value=u'falsch', token=u'falsch', title=u'falsch'),
     SimpleTerm(value=u'richtig', token=u'richtig', title=u'richtig')]
    )

speakervalues = SimpleVocabulary(
    [SimpleTerm(value=u"UK English Female", token=u"UK English Female", title=u"UK Frau Englisch"),
     SimpleTerm(value=u"UK English Male", token=u"UK English Male", title=u"UK Mann Englisch"),
     SimpleTerm(value=u"US English Female", token=u"US English Female", title=u"US Frau Englisch"),
     SimpleTerm(value=u"US English Male", token=u"US English Male", title=u"US Mann Englisch"),
     SimpleTerm(value=u"Deutsch Female", token=u"Deutsch Female", title=u"Frau Deutsch"),
     SimpleTerm(value=u"Deutsch Male", token=u"Deutsch Male", title=u"Mann Deutsch"),
     SimpleTerm(value=u"Spanish Female", token=u"Spanish Female", title=u"Frau Spanisch"),
     SimpleTerm(value=u"Spanish Male", token=u"Spanish Male", title=u"Mann Spanisch"),
     SimpleTerm(value=u"French Female", token=u"French Female", title=u"Frau Französisch"),
     SimpleTerm(value=u"French Male", token=u"French Male", title=u"Mann Französisch"),
     SimpleTerm(value=u"Italian Female", token=u"Italian Female", title=u"Frau Italienisch"),
     SimpleTerm(value=u"Italien Male", token=u"Italien Male", title=u"Mann Italienisch"),
    ])


aufgabenart = SimpleVocabulary(
    [SimpleTerm(value=u'selbsttest', token=u'selbsttest', title=u'Selbsttest'),
     SimpleTerm(value=u'benotet', token=u'benotet', title=u'Benotet')]
    )

def possibleImages(context):
    homefolder = None
    portal = ploneapi.portal.get()
    membersfolder = portal['Members']
    if not ploneapi.user.is_anonymous():
        current = ploneapi.user.get_current()
        username = current.id
        roles = ploneapi.user.get_roles(username=username)
        if not 'Manager' in roles and not 'Site Administrator' in roles:
            pm = getToolByName(portal, 'portal_membership')
            homeurl = pm.getHomeUrl()
            folderid = homeurl.split('/')[-1]
            homefolder = membersfolder[folderid]
    terms = []
    if homefolder:
        homepath = homefolder.getPhysicalPath()
        portalpath = '/'.join(homepath)
        brains = ploneapi.content.find(path=portalpath, portal_type='Image')
        for i in brains:
            if i.portal_type == 'Image':
                terms.append(SimpleVocabulary.createTerm(i.UID, i.UID, i.Title))
    return SimpleVocabulary(terms)
directlyProvides(possibleImages, IContextSourceBinder)


class Antwortoption(Invalid):
    __doc__ = u"Bitte waehle aus, ob die Antwortoption richtig oder falsch ist."

def option_constraint(value):
    """Check that the postcode starts with a 6
    """
    if not value:
        return True
    for i in value:
        if i.get('bewertung') == 'auswahl':
            raise Antwortoption(u"Auswahl, ob die Option richtig oder falsch ist.")
    return True


class IAnswerOptions(model.Schema):
    antwort = schema.TextLine(title=u"Antwort")

    image = schema.Choice(title=u"Bild zur Antwort",
                          source=possibleImages,
                          default=u'educorvi',
                          required=False)

    bewertung = schema.Choice(title=u"Bewertung",
                              vocabulary=wertvalues,
                              required=True)


class SelbstTest(Invalid):
    __doc__ = u"Für Selbsttests musst Du Antwortoptionen eintragen. Textantworten eignen sich nicht für Selbsttests."

class Punkte(Invalid):
    __doc__ = u"Fehler bei der Vergabe von Punkten für diese Aufgabe."


class IVokabeltest(model.Schema):
    title = schema.TextLine(title=u"Überschrift", description=u"Gib dem Vokabeltest eine kurze Überschrift für die Anzeige im Aufgabenordner.")
    art = schema.Choice(title=u"Art der Aufgabenstellung", description=u"Selbsttest dient der selbständigen Wissenskontrolle durch den Schüler.\
                        Bei der benoteten Variante kannst Du über einen QR-Code die Lösungen Deiner Schüler überprüfen.",
                        vocabulary=aufgabenart)

    punkte = schema.Int(title=u"Punkte", description=u"Vergib hier Punkte für eine benotete Aufgabe. Bei Selbsttestaufgaben hier bitte 0 eintragen.",
                        default=0)

    aufforderung = schema.TextLine(title=u'Aufforderung an den Schüler', description=u'Formuliere hier was Dein Schüler tun soll', 
                              default=u"Bitte übersetze auf Deutsch.", required=True) 

    aufgabe = schema.Text(title=u"Wort oder Wortgruppe zur Übersetzung", required=False)

    sprecher = schema.Choice(title=u"Auswahl einer Sprecherstimme", description=u"Ohne Auswahl wird dem Schüler keine Sprecherstimme\
                          angeboten", 
                          required=False, 
                          source=speakervalues)

    dateiaufgabe = NamedBlobFile(title=u"Datei zum Vokabeltest",
                          description=u"Hier kannst Du eine Datei zum Vokabeltest hochladen. Videodateien im mp4-Format\
                          und Audio-Dateien im mp3-Format werden automatisch erkannt und abgespielt wenn der Browser das unterstützt.\
                          Bilder werden direkt im Browser angezeigt.",
                          required=False,)

    antwort = schema.List(title=u"Richtige Antwort(en) / Lösung(en) für diesen Vokabeltest.", description=u"Schreibe jede Lösung, die Du als\
                          richtig bewerten würdest in eine Zeile. Für Selbsttestaufgaben musst Du hier eine\
                          Lösung eingeben.", value_type=schema.TextLine(), required=False)

    upper_lower = schema.Bool(title=u"Bitte hier markieren wenn zwischen Groß- und Kleinschreibung unterschieden werden soll.",
                        default=True)

    bedenkzeit = schema.Int(title=u"Bedenkzeit", description=u"Bitte trage hier eine Bedenkzeit in Sekunden für diesen Test ein. Die Angabe 0\
                        bedeutet: keine Bedenkzeitbeschränkung.",
                        required=True,
                        default=0)

    @invariant
    def validateSelbstTest(data):
        if data.art == 'selbsttest' and data.antwort == '':
            raise SelbstTest(u"Für Selbsttests musst Du eine Antwort bzw. Lösung eintragen.")

    @invariant
    def validatePunkte(data):
        if data.art == 'selbsttest' and data.punkte > 0:
            raise Punkte(u"Für Selbsttestaufgaben kannst Du keine Punkte vergeben.")
        if data.art == 'benotet' and data.punkte == 0:
            raise Punkte(u"Für benotete Aufgaben musst Du angeben wieviel Punkte mit der richtigen Lösung erreicht werden können.")


class Vokabeltest(Item):
    """Content Class"""
