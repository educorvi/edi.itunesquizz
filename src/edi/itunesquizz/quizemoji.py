# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from plone.supermodel import model
from z3c.form import field
from plone.dexterity.browser import edit
from plone.dexterity.browser import add
from plone.namedfile.field import NamedBlobImage
from plone.dexterity.content import Item

class IQuizemoji(model.Schema):
    title = schema.TextLine(title=u"Titel des Quiz-Emoji",
                            required=True)

    image = NamedBlobImage(title=u"Emoji hochladen",
                           required=True)

class Quizemoji(Item):
    """Dexterity Class"""
