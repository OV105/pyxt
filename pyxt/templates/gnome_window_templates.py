#from _pyltfx import *
#from pyxt_exceptions import *
#from pyxt import *
from pyxt import *
from base_window_templates import *
import os
import sys

class GNOMEOpenFileDialogTemplate(OpenFileDialogTemplate):
    __name__ = "GNOMEOpenFileDialogTemplate"
    def build(self):
        OpenFileDialogTemplate.build(self)
        self.widgets['Places'] = Widget(key_alt + 'p')
        self.tests[('Places',)] = {self:event_except_destroyed}
        self.widgets['Search'] = Widget(key_alt + 's')
        self.tests[('Search',)] = {self:event_except_destroyed}

class GNOMESaveFileDialogTemplate(SaveFileDialogTemplate):
    __name__ = "GNOMESaveFileDialogTemplate"
    def build(self):
        SaveFileDialogTemplate.build(self)
        self.widgets['Name'] = Widget(key_alt + 'n')
        self.tests[('Name',)] = {self:event_except_destroyed}
        self.widgets['folder'] = Widget(key_alt + 'f')
        self.tests[('folder',)] = {self:event_except_destroyed}
        self.widgets['Browse'] = Widget(key_alt + 'b')
        self.tests[('Browse',)] = {self:event_except_destroyed}

class AppBrowserDialogTemplate(DialogWindowTemplate):
    __name__ = "AppBrowserDialogTemplate"
    def build(self):
        DialogWindowTemplate.build(self)

class GNOMEAppWindowTemplate(AppWindowTemplate):
    __name__ = "AppWindowTemplate"
    def build(self):
        AppWindowTemplate.build(self)
        self.menu_items[('help','contents')] = MenuItem('c', \
                            parent=self.menu_items[('help')])

        self.tests[('help', 'contents')] = {'Manual':'HelpManualWindowTemplate'}

class GeditAppWindowTemplate(GNOMEAppWindowTemplate):
    __name__ = "GeditAppWindowTemplate"
    def build(self):
        GNOMEAppWindowTemplate.build(self)
        self.menu_items[('edit','select all')] = MenuItem('a', \
                            parent=self.menu_items[('edit')])
        self.menu_items[('search')] = MenuItem(key_alt + 's')
        self.menu_items[('search', 'replace')] = MenuItem('r', \
                            parent=self.menu_items[('search')])

        self.tests[('search', 'replace')] = {'Replace':'GeditReplaceDialog'}

class GeditReplaceDialog(DialogWindowTemplate):
    __name__ = "GeditReplaceDialog"
    def build(self):
        DialogWindowTemplate.build(self)
        self.widgets['Search for'] = Widget(key_alt + 's')
        self.widgets['Replace with'] = Widget(key_alt + 'w')
        self.widgets['Match case'] = Widget(key_alt + 'm')
        self.widgets['Match entire word only'] = Widget(key_alt + 'e')
        self.widgets['Search backwards'] = Widget(key_alt + 'b')
        self.widgets['Wrap around'] = Widget(key_alt + 'w')
        self.widgets['Replace All'] = Widget(key_alt + 'a')
        self.widgets['Replace'] = Widget(key_alt + 'r')
        self.widgets['Find'] = Widget(key_alt + 'f')

