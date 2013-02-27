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
    
    print_layers(sm)
    txts={}
    modified=[]
    
    utilities=sm.getUtilitiesFor(ISubscriberSource)
    utilities2=getAllUtilitiesRegisteredFor(ISubscriberSource)
    
    #
    for cp_item in txt.replace("\r","").split("\n"):
        lst=cp_item.split(":")
        if(len(lst)==2):
            txts[lst[0]]=lst[1]
            t=[a for a in utilities2 if a.name == lst[0]]
            if len(t)==0:
                #if element is not here we suscribe it
                suscribe_utility(sm, lst[1], lst[0])
            elif (lst[1]!=t[0].source):
                #if source is different than before, we notify it as modified
                modified.append(t[0].name.__str__())
                
    for ut in utilities:
        if((ut[0] not in txts.keys()) or (ut[0].__str__() in modified)):
            print "remove utilities %s " % ut[0]
            ut2=sm._utility_registrations.get((ISubscriberSource, ut[0]))
            if ut2 is not None:
                sm.unregisterUtility(ut2, ISubscriberSource, name=ut[0])
            sm.utilities.unsubscribe((), ISubscriberSource, ut[1])
    
    for ut in utilities2:
        if((unicode(ut.name) not in txts.keys()) or (ut.name in modified)):
            print "remove utilities2 %s" % ut.name
            ut2=sm._utility_registrations.get((ISubscriberSource, ut.name))
            if ut2 is not None:
                sm.unregisterUtility(ut2, ISubscriberSource, name=ut.name)
            sm.utilities.unsubscribe((), ISubscriberSource, ut2)

    for i in sm.utilities._adapters[:]:
        s = i.get(ISubscriberSource, {})
        for t in s.keys():
            if((unicode(t) not in txts.keys()) or (t in modified)):
                print "remove adapter %s" % unicode(t)
                sm.unregisterUtility(s[t],ISubscriberSource,name=t.__str__())
                try:
                    sm.utilities.unsubscribe((), ISubscriberSource, s[t])
                    del s[t]
                except:
                    pass
  
    for x in sm._utility_registrations.keys():
        if((x[0].__name__=="ISubscriberSource") and ((unicode(sm._utility_registrations[x][0].name) not in txts.keys()) or (sm._utility_registrations[x][0].name in modified))):
            print "remove _utility_registration %s" % unicode(sm._utility_registrations[x][0].name)
            del sm._utility_registrations[x]

    for m in modified:
        name=unicode(m)
        source=txts[name]
        suscribe_utility(sm, source, name)
        
    transaction.commit()
    sm._p_jar.sync()
    print_layers(sm)

def print_layers(sm):
    print "###"
    print "# _utility_registrations"
    for x in sm._utility_registrations.keys():
        if((x[0].__name__=="ISubscriberSource")):
            print (" > %s (%s) %s" % (sm._utility_registrations[x][0].name,sm._utility_registrations[x][0].source,sm._utility_registrations[x][0]))
    print "# getAllUtilitiesRegisteredFor"
    nlayers = getAllUtilitiesRegisteredFor(ISubscriberSource)
    for a in nlayers:
        print (" => %s (%s) %s" % (a.name,a.source,a))
    print"# getUtilitesFor"
    nlayers = sm.getUtilitiesFor(ISubscriberSource)
    for a in nlayers:
        print (" ==> %s (%s) %s" % (a[1].name,a[1].source,a[1]))
    print "# utilities._subscribers"
    for i in sm.utilities._subscribers[:]:
        s = i.get(ISubscriberSource, {})
        try:
            for t in s[""]:
                print (" ===> %s (%s) %s" % (t.name,t.source,t))
        except:
            pass
    print "###"
    
def suscribe_utility(sm, source, name):
    s = SuscriberSource(source,name)
    print("Creation %s" % name)
    sm.registerUtility(s, ISubscriberSource, name)