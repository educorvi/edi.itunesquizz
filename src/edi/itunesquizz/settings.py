# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout
from z3c.form import form


class IQuizSettings(Interface):
    """ Define settings data structure """

    topexamples = schema.List(title=u"Beispiele für die Bühne",
                              description=u"Trage hier die Webcodes Deiner Beispiele für die Bühne auf der Startseite ein.\
                                           Ein Webcode pro Zeile. Bitte beachte, dass nur Multiple-Choice-Übungen ohne Bilder\
                                           auf der Bühne verwendet werden können.",
                              value_type=schema.TextLine(),
                              required=False)

    examples = schema.List(title=u"Beispiele für die Startseite",
                              description=u"Trage hier die Webcodes Deiner Beispiele für Startseite ein.\
                                           Ein Webcode pro Zeile.",
                              value_type=schema.TextLine(),
                              required=False)


class EdiQuizPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IQuizSettings


EdiQuizPanelView = layout.wrap_form(EdiQuizPanelForm, ControlPanelFormWrapper)
EdiQuizPanelView.label = u"edi.quiz Einstellungen"
