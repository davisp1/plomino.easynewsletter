from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory
from zope.component import adapts, getUtility, adapter, getAdapters

from plone.registry.interfaces import IRecordModifiedEvent

_ = MessageFactory('Plomino.EasyNewsletter')

class ILayer(Interface):
    """Marker interface that defines a Zope 3 browser layer."""

class IEasyNewsletterSettings(Interface):

    easynewsletter_values = schema.Text(title=_(u"Plomino's correspondance for EasyNewsLetter"),
                               description=_(u"Correspondance"),
                               required=False,
                               default=u'',)

@adapter(IEasyNewsletterSettings, IRecordModifiedEvent)
def registry_edited(itema, itemb):
    print itema
