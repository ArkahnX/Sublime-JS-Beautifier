from sublime import error_message, status_message, load_settings, save_settings, packages_path, Region
import sublime_plugin
import re
import os
import sys

try:
    import jsbeautifier
except:
    error_message('Cannot import jsbeautifier!')
    raise

def js_file(view):
    return bool(re.search('JavaScript', view.settings().get('syntax'), re.I))

sublime_settings = 'JS Beautifier.sublime-settings'

class jsbeautifierListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        global sublime_settings
        try:
            settings = load_settings(sublime_settings)
            if js_file(view):
                if settings.get('enabled', True):
                    if view.file_name():
                        self.process(view, settings)
        except Exception, e:
            error_message(str(e))

    def process(self, view, settings):
        replace_region = None
        pos = None
        sel = view.sel()

        if len(sel) == 1:
            region = sel[0]
            if region.empty():  # Get all document
                pos = region.begin()
                replace_region = view.line(
                    Region(0, view.size()))
            else:
                replace_region = view.line(sel[0])
        else:
            return
        content = view.substr(replace_region)

        opts = jsbeautifier.default_options()
        opts.brace_style = settings.get('brace_style', opts.brace_style)
        opts.eval_code = settings.get('eval_code', opts.eval_code)
        opts.indent_char = settings.get('indent_char', opts.indent_char)
        opts.indent_size = settings.get('indent_size', opts.indent_size)
        opts.indent_with_tabs = settings.get('indent_with_tabs', opts.indent_with_tabs)
        opts.jslint_happy = settings.get('jslint_happy', opts.jslint_happy)
        opts.keep_array_indentation = settings.get('keep_array_indentation', opts.keep_array_indentation)
        opts.keep_function_indentation = settings.get('keep_function_indentation', opts.keep_function_indentation)
        opts.max_preserve_newlines = settings.get('max_preserve_newlines', opts.max_preserve_newlines)
        opts.preserve_newlines = settings.get('preserve_newlines', opts.preserve_newlines)
        opts.unescape_strings = settings.get('unescape_strings', opts.unescape_strings)

        fixed = jsbeautifier.beautify(content, opts)
        if fixed != content:
            edit = view.begin_edit()
            view.replace(edit, replace_region, fixed)
            view.end_edit(edit)
            if pos:
                view.sel().clear()
                view.sel().add(pos)
                view.show_at_center(pos)

class jsbeautifierCommand(sublime_plugin.WindowCommand):
    @property
    def settings(self):
        global sublime_settings
        return sublime_settings

class DisableCommand(jsbeautifierCommand):
    def run(self):
        try:
            load_settings(self.settings).set('enabled', False)
            save_settings(self.settings)
            status_message("JS Beautifier Disabled")
        except Exception, e:
            error_message(str(e))

class EnableCommand(jsbeautifierCommand):
    def run(self):
        try:
            load_settings(self.settings).set('enabled', True)
            save_settings(self.settings)
            status_message("JS Beautifier Enabled")
        except Exception, e:
            error_message(str(e))

def package_path():
    filename = os.path.basename(sys.modules[__name__].__file__)
    for parent, dirs, files in os.walk(packages_path()):
        for f in files:
            if filename == f:
                return parent

class DefaultCommand(jsbeautifierCommand):
    def run(self):
        try:
            default = "%s/%s" % (package_path(), self.settings)
            self.window.open_file(default)
        except Exception, e:
            error_message(str(e))

class UserCommand(jsbeautifierCommand):
    def run(self):
        try:
            user = "%s/Users/%s" % (packages_path(), self.settings)
            self.window.open_file(user)
        except Exception, e:
            error_message(str(e))
