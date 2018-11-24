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

ergebnisart = SimpleVocabulary(
    [SimpleTerm(value=u'integer', token=u'integer', title=u'Ganzzahl'),
     SimpleTerm(value=u'intrange', token=u'intrange', title=u'Ganzzahl von|bis'),
     SimpleTerm(value=u'float', token=u'float', title=u'Gleitkommazahl')
     SimpleTerm(value=u'floatrange', token=u'floatrange', title=u'Gleitkommazahl von|bis']
    )

aufgabenart = SimpleVocabulary(
    [SimpleTerm(value=u'selbsttest', token=u'selbsttest', title=u'Selbsttest'),
     SimpleTerm(value=u'benotet', token=u'benotet', title=u'Benotet')]
    )

class IVersuche(form.Schema):
    antwort = schema.TextLine(title=u"Aufgabe oder Messreihe")

    erwartung = schema.Choice(title=u"Ergebniserwartung",
                          vocabulary=ergebnisart)

    ergebnis = schema.TextLine(title=u"Ergebnis",
                              vocabulary=wertvalues,
                              required=True)


class Punkte(Invalid):
    __doc__ = u"Fehler bei der Vergabe von Punkten für diese Aufgabe."


class IExperiment(Interface):
    title = schema.TextLine(title=u"Überschrift", description=u"Gib dem Experiment einen Namen.")
    art = schema.Choice(title=u"Art der Aufgabenstellung", vocabulary=aufgabenart)
    punkte = schema.Int(title=u"Punkte", description=u"Bei Selbsttestaufgaben hier bitte 0 eintragen.", default=0)
    aufgabe = schema.Text(title=u"Versuchsaufbau", description=u"Formuliere hier Deinen Versuchsaufbau und die Aufgabenstellung für das Experiment.")
    image = NamedBlobImage(title=u"Bild zum Versuchsaufbau.", required=False)
    versuchsreihen = schema.List(title=u"Versuchsreihen",
                            description=u"Hier kannst Du angeben, welche Ergebnisse Du in den einzelnen Versuchsreihen erwartest.", 
                            required=True,
                            value_type=DictRow(title=u"Optionen", schema=IVersuche))
    fazit = schema.Bool(title="Fazit",
                        description="Sollen Deine Schüler ein selbständiges Fazit aus dem Experiment ableiten?. Wenn ja, bitte hier klicken.")
    erklaerung = schema.Text(title=u"Erklärung/Lernempfehlung",
                             required=False,
                             description=u"Hier kannst Du Deinen Schülern eine Erklärung zu den Messergebnissen geben oder einen Empfehlung\
                                           zum Weiterlernen geben. Der Text wird mit dem Ergebnis eingeblendet.")


    @invariant
    def validatePunkte(data):
        if data.art == 'selbsttest' and data.punkte > 0:
            raise Punkte(u"Für Selbsttestaufgaben kannst Du keine Punkte vergeben.")
        if data.art == 'benotet' and data.punkte == 0:
            raise Punkte(u"Für benotete Aufgaben musst Du angeben wieviel Punkte mit der richtigen Lösung erreicht werden können.")


class Experiment(Item):
    """Content Class"""


class EditForm(edit.DefaultEditForm):
    fields = field.Fields(IExperiment)
    fields['versuchsreihen'].widgetFactory = DataGridFieldFactory


class AddForm(add.DefaultAddForm):
    portal_type = u"Experiment"
    fields = field.Fields(IExperiment)
    fields['versuchsreihen'].widgetFactory = DataGridFieldFactory


class AddView(add.DefaultAddView):
    form = AddForm
