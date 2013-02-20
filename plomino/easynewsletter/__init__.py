from transaction import commit

from zope.component import getUtility,getGlobalSiteManager
from plone.registry.interfaces import IRegistry

from Products.EasyNewsletter.interfaces import ISubscriberSource

from .browser.interfaces import IEasyNewsletterSettings
from .newsletter import SuscriberSource

external_list=[["/Plone/test-base/testagent","test1"],
           ["/Plone/test-base/testagent","test2"],]

gsm = getGlobalSiteManager()
for source in external_list:
    test = SuscriberSource(source[0])
    gsm.registerUtility(test, ISubscriberSource, source[1])