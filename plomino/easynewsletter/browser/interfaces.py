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
    raw_text=itema.easynewsletter_values

    sm=getSiteManager()
    
    #print_layers(sm)
    texts = {}
    modified = []
    
    utilities = getAllUtilitiesRegisteredFor(ISubscriberSource)
    utilities += [ a[1] for a in sm.getUtilitiesFor(ISubscriberSource) if a[1] not in utilities]
    
    if raw_text is not None:
        for item in raw_text.replace("\r","").split("\n"):
            registry=item.split(":")
            if(len(registry)==2):
                texts[registry[0]]=registry[1]
                found=[a for a in utilities if a.name == registry[0]]
                if len(found)==0:
                    #if element is not here we suscribe it
                    suscribe_utility(sm, registry[1], registry[0])
                elif (registry[1]!=found[0].source):
                    #if source is different than before, we notify it as modified
                    modified.append(found[0].name.__str__())
        
    for ut in utilities:
        if((unicode(ut.name) not in texts.keys()) or (ut.name in modified)):
            ut_registered=sm._utility_registrations.get((ISubscriberSource, ut.name))
            if ut_registered is not None:
                sm.unregisterUtility(ut_registered, ISubscriberSource, name=ut.name)
            sm.utilities.unsubscribe((), ISubscriberSource, ut)

    for adapter in sm.utilities._adapters[:]:
        items = adapter.get(ISubscriberSource, {})
        for key in items.keys():
            if((unicode(key) not in texts.keys()) or (key in modified)):
                del items[key]

    for interface_utility in sm._utility_registrations.keys():
        if((interface_utility[0].__name__=="ISubscriberSource")):
            name=sm._utility_registrations[interface_utility][0].name
            if (((unicode(name) not in texts.keys()) or (name in modified))):
                del sm._utility_registrations[interface_utility]

    for item_modified in modified:
        name=unicode(item_modified)
        source=texts[name]
        suscribe_utility(sm, source, name)
        
    transaction.commit()
    sm._p_jar.sync()
    #print_layers(sm)

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
