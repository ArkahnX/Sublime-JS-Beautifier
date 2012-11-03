from sublime import error_message, load_settings, Region
import sublime_plugin
import re
import settings
from platform import python_version_tuple
v = python_version_tuple()
pip="pip-%s.%s" % (v[0], v[1])

try:
    import jsbeautifier
except:
    error_message('jsbeautifier ImportError, run \nsudo %s install jsbeautifier' % pip)
    raise

def JavaScript(view):
    return bool(re.search('JavaScript', view.settings().get('syntax'), re.I))


def JSON(view):
    return bool(re.search('JSON', view.settings().get('syntax'), re.I))

class jsbeautifierListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        try:
            if JavaScript(view) and not JSON(view):
                if load_settings(settings.filename).get('enabled', True):
                    if view.file_name():
                        self.process(view)
        except Exception, e:
            error_message(str(e))

    def process(self, view):

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
        s = load_settings(settings.filename)
        opts.brace_style = s.get('brace_style', opts.brace_style)
        opts.eval_code = s.get('eval_code', opts.eval_code)
        opts.indent_char = s.get('indent_char', opts.indent_char)
        opts.indent_size = s.get('indent_size', opts.indent_size)
        opts.indent_with_tabs = s.get('indent_with_tabs', opts.indent_with_tabs)
        opts.jslint_happy = s.get('jslint_happy', opts.jslint_happy)
        opts.keep_array_indentation = s.get('keep_array_indentation', opts.keep_array_indentation)
        opts.keep_function_indentation = s.get('keep_function_indentation', opts.keep_function_indentation)
        opts.max_preserve_newlines = s.get('max_preserve_newlines', opts.max_preserve_newlines)
        opts.preserve_newlines = s.get('preserve_newlines', opts.preserve_newlines)
        opts.unescape_strings = s.get('unescape_strings', opts.unescape_strings)

        fixed = jsbeautifier.beautify(content, opts)
        if fixed != content:
            edit = view.begin_edit()
            view.replace(edit, replace_region, fixed)
            view.end_edit(edit)
            if pos:
                view.sel().clear()
                view.sel().add(pos)
                view.show_at_center(pos)
