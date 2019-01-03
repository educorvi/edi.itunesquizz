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
from plone.directives import form
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from plone.namedfile.field import NamedBlobImage
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.contenttypes.interfaces import IImage
from plone import api as ploneapi
from Products.CMFCore.utils import getToolByName
from zope.interface import invariant, Invalid
from zope.interface import directlyProvides
from z3c.form.browser.radio import RadioWidget

wertvalues = SimpleVocabulary(
    [SimpleTerm(value=u'auswahl', token=u'auswahl', title=u'bitte auswählen'),
     SimpleTerm(value=u'falsch', token=u'falsch', title=u'falsch'),
     SimpleTerm(value=u'richtig', token=u'richtig', title=u'richtig')]
    )


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


class IAnswerOptions(form.Schema):
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


class IAufgabe(Interface):
    title = schema.TextLine(title=u"Überschrift", description=u"Gib der Aufgabe eine kurze Überschrift.")
    art = schema.Choice(title=u"Art der Aufgabenstellung", description=u"Bei benoteten Aufgabenstellungen wird ein Barcode generiert.\
                                                                         Dein Schüler muss diesen Barcode mit Dir teilen. Mit diesem Barcode\
                                                                         kannst Du die Lösung Deines Schülers überprüfen",
                        vocabulary=aufgabenart)
    punkte = schema.Int(title=u"Punkte", description=u"Bei Selbsttestaufgaben hier bitte 0 eintragen.", default=0)
    aufgabe = schema.Text(title=u"Aufgabe", description=u"Formuliere hier Deine Fragestellung oder Aufgabe.")
    image = NamedBlobImage(title=u"Bild zur Frage oder Aufgabe", required=False)
    video = schema.Text(title=u"Alternativ: Video zur Frage oder Aufgabe",
                        description=u"Füge hier den Einbettungscode des Videos ein, der von der Video-Plattform bereitgestellt wird.",
                        required=False,)
    antworten = schema.List(title=u"Antwortoptionen",
                            description=u"Hier kannst Du Antwortoptionen für eine Multiple-Choice-Frage eingeben.\
                                          Du musst hier nichts eintragen wenn Du eine Textantwort erwartest.", 
                            required=False,
                            constraint=option_constraint,
                            value_type=DictRow(title=u"Optionen", schema=IAnswerOptions))
    hinweis = schema.Text(title=u"Lösungshinweis",
                          required=False,
                          description=u"Hier kannst Du Deinen Schülern einen Lösungshinweis geben. Der Lösungshinweis\
                                        wird bei der Aufgabenstellung eingeblendet.")
    erklaerung = schema.Text(title=u"Erklärung/Lernempfehlung",
                             required=False,
                             description=u"Hier kannst Du Deinen Schülern eine Erklärung zur Lösung oder einen Empfehlung\
                                           zum Weiterlernen geben. Der Text wird mit dem Ergebnis eingeblendet.")
    solutionimage = NamedBlobImage(title=u"Bild zur Lösung der Aufgabe", required=False)
    solutionvideo = schema.Text(title=u"Alternativ: Video zur Lösung der Frage oder Aufgabe",
                        description=u"Füge hier den Einbettungscode des Videos ein, der von der Video-Plattform bereitgestellt wird.",
                        required=False,)
    bonus = NamedBlobImage(title=u"Bonusbild zur Aufgabe", description=u"Das Bild wird mit einem Barcode kombiniert und angezeigt.\
                                                                         Dein Schüler kann sich das Bilder herunterladen und mit Dir teilen.\
                                                                         Das gilt nur für benotete Aufgabenstellungen.",
                           required=False)


    @invariant
    def validateSelbstTest(data):
        if data.art == 'selbsttest' and data.antworten == []:
            raise SelbstTest(u"Für Selbsttests musst Du Antwortoptionen eintragen. Textantworten eignen sich nicht für Selbsttests.")

    @invariant
    def validatePunkte(data):
        if data.art == 'selbsttest' and data.punkte > 0:
            raise Punkte(u"Für Selbsttestaufgaben kannst Du keine Punkte vergeben.")
        if data.art == 'benotet' and data.punkte == 0:
            raise Punkte(u"Für benotete Aufgaben musst Du angeben wieviel Punkte mit der richtigen Lösung erreicht werden können.")

    @invariant
    def validateAntworten(data):
        if data.antworten:
            for i in data.antworten:
                if i.get('bewertung') == u'auswahl':
                    raise Antwortoption(u"Bitte prüfe Deine Antworten, ob Du richtig oder falsch ausgewählt hast.")

class Aufgabe(Item):
    """Content Class"""


class EditForm(edit.DefaultEditForm):
    fields = field.Fields(IAufgabe)
    fields['antworten'].widgetFactory = DataGridFieldFactory


class AddForm(add.DefaultAddForm):
    portal_type = u"Aufgabe"
    fields = field.Fields(IAufgabe)
    fields['antworten'].widgetFactory = DataGridFieldFactory


class AddView(add.DefaultAddView):
    form = AddForm
