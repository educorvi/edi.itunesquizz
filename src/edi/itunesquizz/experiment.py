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
from z3c.relationfield.schema import RelationChoice
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
     SimpleTerm(value=u'float', token=u'float', title=u'Gleitkommazahl'),
     SimpleTerm(value=u'floatrange', token=u'floatrange', title=u'Gleitkommazahl von|bis')]
    )

aufgabenart = SimpleVocabulary(
    [SimpleTerm(value=u'selbsttest', token=u'selbsttest', title=u'Selbsttest'),
     SimpleTerm(value=u'benotet', token=u'benotet', title=u'Benotet')]
    )

einheiten = SimpleVocabulary(
    [SimpleTerm(value=u's', token=u's', title=u's'),
     SimpleTerm(value=u'm', token=u'm', title=u'm'),
     SimpleTerm(value=u'kg', token=u'kg', title=u'kg'),
     SimpleTerm(value=u'A', token=u'A', title=u'A'),
     SimpleTerm(value=u'V', token=u'V', title=u'V'),
     SimpleTerm(value=u'K', token=u'K', title=u'K'),
     SimpleTerm(value=u'mol', token=u'mol', title=u'mol')]
    )
     

class IVersuche(model.Schema):
    antwort = schema.TextLine(title=u"Text zur Versuchsreihe")

    erwartung = schema.Choice(title=u"Ergebnisart",
                          vocabulary=ergebnisart)

    ergebnis = schema.TextLine(title=u"Ergebniserwartung",
                              required=True)
    einheit = schema.Choice(title=u"Einheit",
                          vocabulary=einheiten,
                          required=False)


class Punkte(Invalid):
    __doc__ = u"Fehler bei der Vergabe von Punkten für diese Aufgabe."

class Fazit(Invalid):
    __doc__ = u"Fehler bei der Anforderung eines Fazits für diese Aufgabe."


class IExperiment(model.Schema):
    title = schema.TextLine(title=u"Überschrift", description=u"Titel des Experiments.")
    art = schema.Choice(title=u"Art des Experiments", description=u"Selbsttest dient der selbständigen Ergebniskontrolle durch den Schüler.\
                        Bei der benoteten Variante kannst Du über einen QR-Code die Ergebnisse Deiner Schüler überprüfen.",
                        vocabulary=aufgabenart)
    punkte = schema.Int(title=u"Punkte", description=u"Bei Selbsttestaufgaben hier bitte 0 eintragen.", default=0)
    aufgabe = schema.Text(title=u"Versuchsaufbau", description=u"Formuliere hier Deinen Versuchsaufbau und die Aufgabenstellung für das Experiment.")

    model.fieldset(
        'extras',
        label=u"Extras zum Experiment",
        fields=['image', 'video', 'erklaerung']
    )

    image = NamedBlobImage(title=u"Bild zum Versuchsaufbau", description=u"Erscheint unterhalb der Aufgabenstellung für das Experiment", 
                           required=False)
    video = schema.Text(title=u"Alternativ: Video zum Versuchsaufbau",
                        description=u"Füge hier den Einbettungscode des Videos ein, der von der Video-Plattform bereitgestellt wird.",
                        required=False,)
    form.widget('versuchsreihen', DataGridFieldFactory)
    versuchsreihen = schema.List(title=u"Versuchsreihen",
                            description=u"Hier kannst Du angeben, welche Ergebnisse Du in den einzelnen Versuchsreihen erwartest.", 
                            required=True,
                            value_type=DictRow(title=u"Optionen", schema=IVersuche),
                            default=[{'antwort':'z.B. Bremsweg bei 30km/h', 'erwartung':'floatrange', 'ergebnis':'4,5|9,0', 'einheit':'m'}])
    fazit = schema.Bool(title=u"Fazit des Schülers erwünscht",
                        description=u"Auswahl setzt ein zusätzliches Freitextfeld unterhalb der Ergebnistabelle (nur für benotete Experimente).")
    erklaerung = schema.Text(title=u"Erklärung/Lernempfehlung",
                             required=False,
                             description=u"Nur relevant für Selbsttest-Aufgaben. Der Text wird zusammen mit dem Ergebnis eingeblendet.")
    bonus = NamedBlobImage(title=u"Bonusbild zum QR-Code", description=u"Bei benoteten Aufgaben wird Dein Bild mit dem Barcode kombiniert\
                           und dem Schüler zum Download bereitgestellt.",
                           required=False)


    @invariant
    def validatePunkte(data):
        if data.art == 'selbsttest' and data.punkte > 0:
            raise Punkte(u"Für Selbsttest-Experimente kannst Du keine Punkte vergeben.")
        if data.art == 'benotet' and data.punkte == 0:
            raise Punkte(u"Für benotete Experimente musst Du angeben wieviel Punkte mit der richtigen Lösung erreicht werden können.")

    @invariant
    def validateFazit(data):
        if data.art == 'selbsttest' and data.fazit == True:
            raise Fazit(u"Für Selbsttest-Experimente darfst Du Deinen Schüler kein Fazit ableiten lassen.")


class Experiment(Item):
    """Content Class"""


#class EditForm(edit.DefaultEditForm):
#    fields = field.Fields(IExperiment)
#    fields['versuchsreihen'].widgetFactory = DataGridFieldFactory


#class AddForm(add.DefaultAddForm):
#    portal_type = u"Experiment"
#    fields = field.Fields(IExperiment)
#    fields['versuchsreihen'].widgetFactory = DataGridFieldFactory


#class AddView(add.DefaultAddView):
#    form = AddForm
