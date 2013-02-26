from zope import schema
from zope.interface import Interface
import transaction

from zope.i18nmessageid import MessageFactory
from zope.component import adapts, getUtility, adapter, getAdapters, getUtilitiesFor, getAllUtilitiesRegisteredFor, getGlobalSiteManager, getSiteManager
from zope.component import getSiteManager
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
    
    print_layers(sm)
    """
    for x in sm._utility_registrations.keys():
        if((x[0].__name__=="ISubscriberSource")):
            del sm._utility_registrations[x]
            transaction.commit()
    """
    txts={}
    #layers = getAllUtilitiesRegisteredFor(ISubscriberSource)
    
    utilities=sm.getUtilitiesFor(ISubscriberSource)
    
    for cp_item in txt.replace("\r","").split("\n"):
        lst=cp_item.split(":")
        if(len(lst)==2):
            txts[lst[0]]=lst[1]
            #if len([a for a in layers if a.name == lst[0]])==0:
            suscribe_utility(sm, lst[1], lst[0])



    for ut in utilities:
        key=ut[0].__str__()
        if(key.__str__() not in txt):
            ut2=sm._utility_registrations.get((ISubscriberSource, ut[0]))
            if ut2 is not None:
                sm.unregisterUtility(ut2, ISubscriberSource, name=ut[0])
            print(ut)
            sm.utilities.unsubscribe((), ISubscriberSource, ut[1])


    #import pdb; pdb.set_trace();
    """
    for ut in layers:
        if(ut.name not in txt):
            ut = layers[-1]
            name = ut.name
            #cpt = [a for a in layers if a.name == ut.name]
            sm.unregisterUtility(ut, ISubscriberSource, name=ut.name)
            for i in sm.utilities._subscribers[:]:
                s = i.get(ISubscriberSource, {})
                for j in s.keys()[:]:
                    s[j] = tuple([a 
                                  for a in s[j] 
                                  if not a is ut])              
            #sm.utilities.unsubscribe((), ISubscriberSource)
            #if ISubscriberSource in sm.utilities.__dict__['_provided']:
            #    del sm.utilities.__dict__['_provided'][ISubscriberSource]
            del ut
    """
    #if ISubscriberSource in sm.utilities.__dict__['_provided']:
    #    del sm.utilities.__dict__['_provided'][ISubscriberSource]
        
    #transaction.commit()        

    for i in sm.utilities._adapters[:]:
        s = i.get(ISubscriberSource, {})
        for t in s.keys():
            if(t.__str__() not in txt):
                sm.unregisterUtility(s[t],ISubscriberSource,name=t.__str__())
                sm.utilities.unsubscribe((), ISubscriberSource, s[t])
                del s[t]

    for x in sm._utility_registrations.keys():
        if((x[0].__name__=="ISubscriberSource")):
            del sm._utility_registrations[x]
            transaction.commit()
            
    sm.utilities.changed(None)

    transaction.commit()
    sm._p_jar.sync()
    print_layers(sm)
    #sm._p_jar.sync()

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


