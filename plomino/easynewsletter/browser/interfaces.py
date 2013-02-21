from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory
from zope.component import adapts, getUtility, adapter, getAdapters, getAllUtilitiesRegisteredFor, getGlobalSiteManager

from plone.registry.interfaces import IRecordModifiedEvent
from Products.EasyNewsletter.interfaces import ISubscriberSource
from plomino.easynewsletter.newsletter import SuscriberSource

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
    txt=itema.easynewsletter_values
    layers = getAllUtilitiesRegisteredFor(ISubscriberSource)
    sm=getGlobalSiteManager()
    txts={}
    
    for cp_item in txt.replace("\r","").split("\n"):
        lst=cp_item.split(":")
        if(len(lst)==2):
            txts[lst[0]]=lst[1]
            
    for name in txts.keys():
        found=False
        for item in layers:
            if item.name==name:
                found=True
                if item.source!=txts[name]:
                    sm.unregisterUtility(item, ISubscriberSource, name=item.name)
                    suscribe_global_utility(sm, txts[name], name)
        if not found:
                    suscribe_global_utility(sm, txts[name], name)
                    
    for item in layers:
        if(item.name not in txt):
            sm.unregisterUtility(item, ISubscriberSource, name=item.name)


def suscribe_global_utility(sm,source,name):
        s=SuscriberSource(source,name)
        sm.registerUtility(s, ISubscriberSource, name)