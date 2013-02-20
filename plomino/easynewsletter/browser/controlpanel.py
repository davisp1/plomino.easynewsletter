from plone.app.registry.browser import controlpanel

from plomino.easynewsletter.interfaces import IEasyNewsletterSettings, _

class EasyNewsletterSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IEasyNewsletterSettings
    label = _(u"EasyNewsletter Plomino settings")
    description = _(u"""""")

    def updateFields(self):
        super(EasyNewsletterSettingsEditForm, self).updateFields()
    
    def updateWidgets(self):
        super(EasyNewsletterSettingsEditForm, self).updateWidgets()

class EasyNewsletterSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = EasyNewsletterSettingsEditForm
