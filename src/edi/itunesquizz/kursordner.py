from zope.interface import Interface
from zope import schema
from plone.dexterity.content import Container

class IKursordner(Interface):

    id = schema.TextLine(title=u"iTunes U Kursnummer")
    email = schema.TextLine(title=u'E-Mail-Adresse', description=u"An diese E-Mail-Adresse werden alle Ergebnisse der benoteten Aufgaben\
                                                                   geschickt")

class Kursordner(Container):
    """Dexterity Class"""

