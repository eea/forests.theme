from forests.theme.interfaces import IMosaicSettings
from plone.app.registry.browser.controlpanel import (ControlPanelFormWrapper,
                                                     RegistryEditForm)
from plone.z3cform import layout
from z3c.form import form


class MosaicSettingsForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IMosaicSettings


MosaicSettingsView = layout.wrap_form(
    MosaicSettingsForm,
    ControlPanelFormWrapper
)
MosaicSettingsView.label = u"Volto Mosaic Settings"
