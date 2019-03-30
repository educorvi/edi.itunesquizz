# -*- coding: utf-8 -*-
from zope.interface import provider
from zope.interface import Interface
from zope import schema
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
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

class IQuizSettings(Interface):
    """ Define settings data structure """

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
