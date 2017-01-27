#from _pyltfx import *
#from pyxt_exceptions import *
#from pyxt import *
from pyxt import *
import os
import sys

class DialogWindowTemplate(WindowTemplate):
    __name__ = "DialogWindowTemplate"
    def build(self):
        self.widgets['Close'] = Widget(key_esc)
        self.tests[('Close',)] = {self:event_destroyed}

    def clearTextField(self):
        cmd = self.getCmd(key_home + key_shift + key_end + key_bksp)
        cmd.execute(delay=self.text_delay)

    def textField(self, text):
        self.clearTextField()
        self.enterText(text)

class FileDialogTemplate(DialogWindowTemplate):
    __name__ = "FileDialogTemplate"
    def build(self):
        #self.widgets['Cancel'] = key_esc
        DialogWindowTemplate.build(self)
        self.widgets['Cancel'] = Widget(key_alt + 'c')
        self.tests[('Cancel',)] = {self:event_destroyed}

class OpenFileDialogTemplate(FileDialogTemplate):
    __name__ = "OpenFileDialogTemplate"
    def build(self):
        FileDialogTemplate.build(self)
        self.widgets['Open'] = Widget(key_alt + 'o')
        self.tests[('Open',)] = {self:event_destroyed}
        self.widgets['Location'] = Widget(key_alt + 'l')
        self.tests[('Location',)] = {self:event_except_destroyed}

class SaveFileDialogTemplate(FileDialogTemplate):
    __name__ = "SaveFileDialogTemplate"
    def build(self):
        FileDialogTemplate.build(self)
        self.widgets['Save'] = Widget(key_alt + 's')
        self.tests[('Save',)] = {self:event_destroyed}

class HelpAboutDialogTemplate(DialogWindowTemplate):
    __name__ = "HelpAboutDialogTemplate"
    def build(self):
        self.widgets['Close'] = Widget(key_esc)
        self.widgets['Credits'] = Widget(key_alt + 'r')
        #self.widgets['Close'] = key_alt + 'c' 
        self.tests[('Close',)] = {self:event_destroyed}
        self.tests[('Credits',)] = {'Credits':'DialogWindowTemplate'}

class AppWindowTemplate(WindowTemplate):
    __name__ = "AppWindowTemplate"
    def build(self):
        # (menu):("command", 
        self.menu_items[('file')] = MenuItem(key_alt+'f')
        self.menu_items[('file', 'open')] = MenuItem('o', \
                               parent=self.menu_items[('file')])
        self.menu_items[('file', 'save')] = MenuItem('s', \
                               parent=self.menu_items[('file')])
        self.menu_items[('file', 'save as')] = MenuItem('a', \
                               parent=self.menu_items[('file')])
        self.menu_items[('file', 'close')] = MenuItem('c', \
                               parent=self.menu_items[('file')])
        self.menu_items[('file', 'quit')] = MenuItem('q', \
                               parent=self.menu_items[('file')],
                               shortcut=key_ctrl + 'q')
        self.menu_items[('help')] = MenuItem(key_alt + 'h')
        self.menu_items[('help', 'about')] = MenuItem('a', \
                               parent=self.menu_items[('help')])
        self.menu_items[('edit')] = MenuItem(key_alt+'e')
        self.menu_items[('edit','copy')] = MenuItem('c', \
                               parent=self.menu_items[('edit')])
        self.menu_items[('edit','cut')] = MenuItem('t', \
                               parent=self.menu_items[('edit')])
        self.menu_items[('edit','paste')] = MenuItem('p', \
                               parent=self.menu_items[('edit')])

        self.tests[('file', 'open')] = {'Open':'OpenFileDialogTemplate'}
        self.tests[('file', 'save')] = {'Save':'SaveFileDialogTemplate'}
        self.tests[('file', 'save as')] = {'Save':'SaveFileDialogTemplate'}
        #self.tests[('file', 'close')] = {self:event_except_destroyed}
        #FIXME may exit
        self.tests[('file', 'quit')] = {self:event_destroyed}
        self.tests[('help', 'about')] = {'About':'HelpAboutDialogTemplate'}
        #self.tests[('edit', 'copy')] = {self:event_except_destroyed}
        #self.tests[('edit', 'cut')] = {self:event_except_destroyed}
        #self.tests[('edit', 'paste')] = {self:event_except_destroyed}

class HelpManualWindowTemplate(AppWindowTemplate):
    __name__ = "HelpManualWindowTemplate"
    def build(self):
        del(self.menu_item[('file', 'open')])
        del(self.menu_item[('file', 'save')])
        del(self.menu_item[('file', 'save as')])
        del(self.menu_item[('edit', 'cut')])
        del(self.menu_item[('edit', 'paste')])
        
        del(self.tests[('file', 'open')])
        del(self.tests[('file', 'save')])
        del(self.tests[('file', 'save as')])
        del(self.tests[('edit', 'cut')])
        del(self.tests[('edit', 'paste')])
