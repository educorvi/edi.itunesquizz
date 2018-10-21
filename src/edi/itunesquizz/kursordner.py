from zope.interface import Interface
from zope import schema
from plone.supermodel import model
from z3c.form import field
from plone.dexterity.browser import edit
from plone.dexterity.browser import add
from plone.dexterity.content import Container

class IKursordner(Interface):
    title = schema.TextLine(title=u"iTunes U Kursnummer")
    description = schema.Text(title=u"Kurzbeschreibung des Kurses", required=False)
    email = schema.TextLine(title=u'E-Mail-Adresse', description=u"An diese E-Mail-Adresse werden alle Ergebnisse der benoteten Aufgaben\
                                                                   geschickt")

class Kursordner(Container):
    """Dexterity Class"""


class EditForm(edit.DefaultEditForm):
    fields = field.Fields(IKursordner)


class AddForm(add.DefaultAddForm):
    portal_type = u"Kursordner"
    fields = field.Fields(IKursordner)


class AddView(add.DefaultAddView):
    form = AddForm
