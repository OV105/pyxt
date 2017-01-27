from pyxt import *
from base_window_templates import *

class KDEAppWindowTemplate(AppWindowTemplate):
    __name__ = "KDEAppWindowTemplate"
    def build(self):
        AppWindowTemplate.build(self)
        self.menu_items[('help','about kde')] = MenuItem('k', \
            parent=self.menu_items[('help')])
        self.menu_items[('settings')] = MenuItem(key_alt + 's') 
        self.menu_items[('settings', 'configure shortcuts')] = MenuItem('h', \
            parent=self.menu_items[('settings')])
        self.menu_items[('settings', 'configure toolbars')] = MenuItem('b', \
            parent=self.menu_items[('settings')])
        self.menu_items[('settings', 'configure kde')] = MenuItem('c', \
            parent=self.menu_items[('settings')])

        self.tests[('help', 'about kde')] = {'About KDE':'KDEAboutHelpDialog'}
        self.tests[('settings', 'configure shortcuts')] = \
                {'Configure Shortcuts':'KDEConfigureShortcutsDialog'}
        self.tests[('settings', 'configure toolbars')] = \
                {'Configure Toolbars':'KDEConfigureToolbarsDialog'}
        self.tests[('settings', 'configure kde')] = \
                {'Settings':'KDEConfigureKDEDialog'}


class KateAppWindowTemplate(KDEAppWindowTemplate):
    __name__ = "KateAppWindowTemplate"
    def build(self):
        KDEAppWindowTemplate.build(self)

class KDEAboutHelpDialog(DialogWindowTemplate):
    __name__ = "KDEAboutHelpDialog"
    def build(self):
        DialogWindowTemplate.build(self)
        self.widgets['Help'] = Widget(key_alt + 'h')

        self.tests[('Help')] = {'.*':'HelpWindow'}
        

class KDEConfigureDialog(DialogWindowTemplate):
    __name__ = "KDEConfigureDialog"
    def build(self):
        DialogWindowTemplate.build(self)

    def build(self):
        self.widgets['OK'] = Widget(key_alt + 'o')
        self.widgets['Defaults'] = Widget(key_alt + 'd')
        self.widgets['Cancel'] = Widget(key_alt + 'c')

        self.tests[('OK')] = {self:event_destroyed}
        self.tests[('Cancel')] = {self:event_destroyed}

class KDEConfigureShortcutsDialog(KDEConfigureDialog):
    __name__ = "KDEConfigureShortcutsDialog"
    def build(self):
        KDEConfigureDialog.build(self)

class KDEConfigureToolbarsDialog(KDEConfigureDialog):
    __name__ = 'KDEConfigureToolbarsDialog'
    def build(self):
        KDEConfigureDialog.build(self)


class KDEConfigureKDEDialog(KDEConfigureDialog):
    __name__ = 'KDEConfigureKDEDialog'
    def build(self):
        KDEConfigureDialog.build(self)
        self.widgets.pop('Defaults')
