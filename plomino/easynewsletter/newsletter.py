from zope.interface import implements
import logging

from Products.EasyNewsletter.interfaces import ISubscriberSource

logger = logging.getLogger('newsletter')

class SuscriberSource(object):
    implements(ISubscriberSource)
    
    def __init__(self,source,name):
        self.source=source
        self.name=name
        
    def getSubscribers(self, newsletter):
        """ return all subscribers for the given newsletter. 
            Newsletter subscriptions are referenced through UIDs.
        """
        uid = newsletter.UID()
        try:
            agent=newsletter.restrictedTraverse(self.source.split("/"))
            a=agent()
        except:
            a=[]
        return a
