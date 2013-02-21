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
        """ return all subscribers for the given newsletter
            from the MyInfo user database. Newsletter subscriptions
            are referenced inside MyInfo through UIDs.
        """
        uid = newsletter.UID()
        subscribers = list()
        agent=newsletter.restrictedTraverse(self.source)
        a=agent()
        return a
