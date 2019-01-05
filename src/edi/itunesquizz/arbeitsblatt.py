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
from plone.app.textfield import RichText

aufgabenart = SimpleVocabulary(
    [SimpleTerm(value=u'selbsttest', token=u'selbsttest', title=u'Selbsttest'),
     SimpleTerm(value=u'benotet', token=u'benotet', title=u'Benotet')]
    )

def possibleArticle(context):
    homefolder = None
    portal = ploneapi.portal.get()
    membersfolder = portal['Members']
    if not ploneapi.user.is_anonymous():
        current = ploneapi.user.get_current()
        username = current.id
        roles = ploneapi.user.get_roles(username=username)
        if not 'Manager' in roles and not 'Site Administrator' in roles:
            pm = getToolByName(portal, 'portal_membership')
            homeurl = pm.getHomeUrl()
            folderid = homeurl.split('/')[-1]
            homefolder = membersfolder[folderid]
    terms = []
    if homefolder:
        homepath = homefolder.getPhysicalPath()
        portalpath = '/'.join(homepath)
        brains = ploneapi.content.find(path=portalpath, portal_type=['Aufgabe', 'Experiment'])
        for i in brains:
            obj = i.getObject()
            mytype = i.portal_type
            if mytype == 'Aufgabe':
                mytype = u'Übung'
            titel = '%s (%s - %s)' %(obj.title, mytype, obj.art)
            terms.append(SimpleVocabulary.createTerm(i.UID, i.UID, titel))
    return SimpleVocabulary(terms)
directlyProvides(possibleArticle, IContextSourceBinder)


class SelbstTest(Invalid):
    __doc__ = u"Die Art des Arbeitsblattes muss zu den ausgwählten Aufgabenstellungen passen."

class IArbeitsblatt(Interface):
    title = schema.TextLine(title=u"Überschrift", description=u"Titel des Arbeitsblattes")
    description = schema.Text(title=u"Kurzbeschreibung", required=False)
    art = schema.Choice(title=u"Art des Arbeitsblattes", description=u"Selbsttest dient der selbständigen Wissenskontrolle durch den Schüler.\
                        Bei der benoteten Variante kannst Du über einen QR-Code die Lösungen Deiner Schüler überprüfen.",
                        vocabulary=aufgabenart)

    textvor = RichText(title=u"Prolog", description=u"Hier kannst Du Text vor die Übungen und Experimente setzen.", required=False)
    parts = schema.List(title=u"Übungen und Experimente auswählen", description=u"Beachte: Bei einem benoteten Arbeitsblatt\
                        verwendest Du nur benotete Aufgabentypen, bei einem Selbsttest-Arbeitsblatt ausschließlich\
                        Selbsttest-Aufgabentypen.",
                        value_type=schema.Choice(source=possibleArticle))
    textnach = RichText(title=u"Epilog", description=u"Hier kannst Du Text im Anschluss an die Übungen und Experimente setzen.", required=False)

    bonus = NamedBlobImage(title=u"Bonusbild zum QR-Code", description=u"Bei einem benoteten Arbeitsblatt wird Dein Bild mit dem Barcode kombiniert\
                        und dem Schüler zum Download bereitgestellt.",
                        required=False)


    @invariant
    def validateSelbstTest(data):
        for i in data.parts:
            testobj = ploneapi.content.get(UID = i)
            if testobj.art != data.art:
                message="Die Art des Arbeitsblattes ist %s. Die Aufgabe %s ist vom Typ: %s. Das passt leider nicht zusammen." % (data.art,
                                                                                                                                 testobj.title,
                                                                                                                                 testobj.art)
                                                                                                                                 
                raise SelbstTest(message)
   
class Arbeitsblatt(Item):
    """Content Class"""


#class EditForm(edit.DefaultEditForm):
#    fields = field.Fields(IAufgabe)
#    fields['antworten'].widgetFactory = DataGridFieldFactory


#class AddForm(add.DefaultAddForm):
#    portal_type = u"Aufgabe"
#    fields = field.Fields(IAufgabe)
#    fields['antworten'].widgetFactory = DataGridFieldFactory


#class AddView(add.DefaultAddView):
#    form = AddForm
