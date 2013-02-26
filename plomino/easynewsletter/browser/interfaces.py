import transaction

from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.component import adapter, getUtilitiesFor, getAllUtilitiesRegisteredFor, getSiteManager

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

    sm=getSiteManager()
    
    #print_layers(sm)
    txts={}
    
    utilities=sm.getUtilitiesFor(ISubscriberSource)
    utilities2=getAllUtilitiesRegisteredFor(ISubscriberSource)
    
    for cp_item in txt.replace("\r","").split("\n"):
        lst=cp_item.split(":")
        if(len(lst)==2):
            txts[lst[0]]=lst[1]
            if len([a for a in utilities if a[0] == lst[0]])==0:
                suscribe_utility(sm, lst[1], lst[0])

    for ut in utilities:
        key=ut[0].__str__()
        if(key.__str__() not in txt):
            ut2=sm._utility_registrations.get((ISubscriberSource, ut[0]))
            if ut2 is not None:
                sm.unregisterUtility(ut2, ISubscriberSource, name=ut[0])
            sm.utilities.unsubscribe((), ISubscriberSource, ut[1])
    
    for ut in utilities2:
        if(ut.name not in txt):
            ut2=sm._utility_registrations.get((ISubscriberSource, ut.name))
            if ut2 is not None:
                sm.unregisterUtility(ut2, ISubscriberSource, name=ut.name)
            sm.utilities.unsubscribe((), ISubscriberSource, ut2)

    for i in sm.utilities._adapters[:]:
        s = i.get(ISubscriberSource, {})
        for t in s.keys():
            if(t.__str__() not in txt):
                sm.unregisterUtility(s[t],ISubscriberSource,name=t.__str__())
                try:
                    sm.utilities.unsubscribe((), ISubscriberSource, s[t])
                    del s[t]
                except:
                    pass
  
    for x in sm._utility_registrations.keys():
        if((x[0].__name__=="ISubscriberSource") and ( sm._utility_registrations[x][0].name not in txts.keys())):
            del sm._utility_registrations[x]

    transaction.commit()
    sm._p_jar.sync()
    #print_layers(sm)

def print_layers(sm):
    print "###"
    for x in sm._utility_registrations.keys():
        if((x[0].__name__=="ISubscriberSource")):
            print " > "+sm._utility_registrations[x][0].name+" "+sm._utility_registrations[x][0].__str__()
    print""
    nlayers = getAllUtilitiesRegisteredFor(ISubscriberSource)
    for a in nlayers:
        print " => "+a.name+" "+a.__str__()
    print""
    nlayers = sm.getUtilitiesFor(ISubscriberSource)
    for a in nlayers:
        print " ==> "+a.__str__()
    print""
    for i in sm.utilities._subscribers[:]:
        s = i.get(ISubscriberSource, {})
        try:
            for t in s[""]:
                print " ===> "+t.name+" "+t.__str__()
        except:
            pass
    print "###"
    
def suscribe_utility(sm, source, name):
    s = SuscriberSource(source,name)
    print name
    sm.registerUtility(s, ISubscriberSource, name)


