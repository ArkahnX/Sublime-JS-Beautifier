from sublime import error_message, status_message, load_settings, save_settings, packages_path
from sublime_plugin import WindowCommand
import os
import sys
import settings

def package_path():
    filename = os.path.basename(sys.modules[__name__].__file__)
    for parent, dirs, files in os.walk(packages_path()):
        for f in files:
            if filename == f:
                return parent

class DisableCommand(WindowCommand):
    def run(self):
        try:
            load_settings(settings.filename).set('enabled', False)
            save_settings(settings.filename)
            status_message("JS Beautifier Disabled")
        except Exception, e:
            error_message(str(e))

class EnableCommand(WindowCommand):
    def run(self):
        try:
            load_settings(settings.filename).set('enabled', True)
            save_settings(settings.filename)
            status_message("JS Beautifier Enabled")
        except Exception, e:
            error_message(str(e))

class DefaultCommand(WindowCommand):
    def run(self):
        try:
            default = "%s/%s" % (package_path(), settings.filename)
            self.window.open_file(default)
        except Exception, e:
            error_message(str(e))

class UserCommand(WindowCommand):
    def run(self):
        try:
            user = "%s/User/%s" % (packages_path(), settings.filename)
            self.window.open_file(user)
        except Exception, e:
            error_message(str(e))