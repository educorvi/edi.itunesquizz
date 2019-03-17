# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from plone.supermodel import model
from z3c.form import field
from plone.dexterity.browser import edit
from plone.dexterity.browser import add
from plone.namedfile.field import NamedBlobImage
from plone.dexterity.content import Container

class IBeispielordner(model.Schema):
    title = schema.TextLine(title=u"Titel",)

    description = schema.Text(title=u"Kurzbeschreibung", required=False)

    image = NamedBlobImage(title=u"Bild zum Beispielordner",
                           required=False)

class Beispielordner(Container):
    """Dexterity Class"""
