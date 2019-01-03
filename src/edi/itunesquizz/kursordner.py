# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema
from plone.supermodel import model
from z3c.form import field
from plone.dexterity.browser import edit
from plone.dexterity.browser import add
from plone.namedfile.field import NamedBlobImage
from plone.dexterity.content import Container

class IKursordner(model.Schema):
    title = schema.TextLine(title=u"Kurs-ID",
                            description=u"ID aus dazugehörigem Kurs oder neue ID eintragen")

    description = schema.Text(title=u"Kurzbeschreibung", required=False)

    image = NamedBlobImage(title=u"Bild zum Aufgabenordner",
                           required=False)



class Kursordner(Container):
    """Dexterity Class"""
