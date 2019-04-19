# -*- coding: utf-8 -*-
from zope.interface import provider
from zope.interface import Interface
from zope import schema
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.namedfile.field import NamedImage
from plone.z3cform import layout
from z3c.form import form
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from plone import api as ploneapi

def make_terms(items):
    """ Create zope.schema terms for vocab from tuples """
    terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
    return terms

@provider(IVocabularyFactory)
def example_tasks(context):
    brains = ploneapi.content.find(portal_type='Aufgabe', Beispiel=True)
    result = [(brain['UID'], '%s (%s)' %(brain['Title'], brain['Creator'])) for brain in brains]
    terms = make_terms(result)
    return SimpleVocabulary(terms)

@provider(IVocabularyFactory)
def quiz_emojis(context):
    brains = ploneapi.content.find(portal_type='Quizemoji', published=True)
    result = [(brain['UID'], '%s' %brain['Title']) for brain in brains]
    terms = make_terms(result)
    return SimpleVocabulary(terms)
 

class IQuizSettings(Interface):
    """ Define settings data structure """

    isquizsite = schema.Bool(title=u"Aktivieren wenn es sich um eine edi.quiz Site handelt.",
                             description=u"Damit werden alle Viewlet-Elemente der Quiz-Site aktiviert",
                             default=False)

    emoji = schema.Bool(title=u"Aktivieren, wenn Emojis bei den Ergebnissen der Aufgabenstellungen  angezeigt weden sollen.",
                             default=True)

    true_emoji = schema.Choice(title=u"Emoji für erfolgreich gelöste Aufgaben.", vocabulary='quiz.emojis',required=False)

    false_emoji = schema.Choice(title=u"Emoji für fehlerhaft gelöste Aufgaben.", vocabulary='quiz.emojis', required=False)

    topexamples = schema.List(title=u"Beispiele für die Bühne",
                              description=u"Wähle hier die Beispiele für die Bühne auf der Startseite aus.",
                              value_type=schema.Choice(vocabulary='example.tasks'),
                              required=False)

    examples = schema.List(title=u"Beispiele für die Startseite",
                              description=u"Trage hier die Webcodes Deiner Beispiele für Startseite ein.\
                                           Ein Webcode pro Zeile.",
                              value_type=schema.Choice(vocabulary='example.tasks'),
                              required=False)


class EdiQuizPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IQuizSettings


EdiQuizPanelView = layout.wrap_form(EdiQuizPanelForm, ControlPanelFormWrapper)
EdiQuizPanelView.label = u"edi.quiz Einstellungen"
