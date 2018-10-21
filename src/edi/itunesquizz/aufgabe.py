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
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import invariant, Invalid

wertvalues = SimpleVocabulary(
    [SimpleTerm(value=u'falsch', token=u'falsch', title=u'falsch'),
     SimpleTerm(value=u'richtig', token=u'richtig', title=u'richtig')]
    )


aufgabenart = SimpleVocabulary(
    [SimpleTerm(value=u'selbsttest', token=u'selbsttest', title=u'Selbsttest'),
     SimpleTerm(value=u'benotet', token=u'benotet', title=u'Benotet')]
    )


class IAnswerOptions(Interface):
    antwort = schema.TextLine(title=u"Antwort")
    bewertung = schema.Choice(title=u"Bewertung", vocabulary=wertvalues, required=True, default=u'falsch')


class SelbstTest(Invalid):
    __doc__ = u"Für Selbsttests musst Du Antwortoptionen eintragen. Textantworten eignen sich nicht für Selbsttests."

class Punkte(Invalid):
    __doc__ = u"Fehler bei der Vergabe von Punkten für diese Aufgabe."


class IAufgabe(Interface):
    title = schema.TextLine(title=u"Überschrift", description=u"Gib der Aufgabe eine kurze Überschrift.")
    art = schema.Choice(title=u"Art der Aufgabenstellung", vocabulary=aufgabenart)
    punkte = schema.Int(title=u"Punkte", description=u"Bei Selbsttestaufgaben hier bitte 0 eintragen.", default=0)
    aufgabe = schema.Text(title=u"Aufgabe", description=u"Formuliere hier Deine Fragestellung oder Aufgabe.")
    antworten = schema.List(title=u"Antwortoptionen", 
                            description=u"Hier kannst Du Antwortoptionen für eine Multiple-Choice-Frage eingeben.\
                                          Du musst hier nichts eintragen wenn Du eine Textantwort erwartest.", 
                            required=False,
                            value_type=DictRow(title=u"Optionen", schema=IAnswerOptions))
    hinweis = schema.Text(title=u"Lösungshinweis",
                          required=False,
                          description=u"Hier kannst Du Deinen Schülern einen Lösungshinweis geben. Der Lösungshinweis\
                                        wird bei der Aufgabenstellung eingeblendet.")
    erklaerung = schema.Text(title=u"Erklärung/Lernempfehlung",
                             required=False,
                             description=u"Hier kannst Du Deinen Schülern eine Erklärung zur Lösung oder einen Empfehlung\
                                           zum Weiterlernen geben. Der Text wird mit dem Ergebnis eingeblendet.")


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
