import os
import tw2.core as twc
import tw2.forms as twf
from markupsafe import Markup, escape_silent


__all__ = ['CodeMirrorEditor', 'CodeMirrorDisplay']


codemirror_js = twc.JSLink(
    modname=__name__,
    filename='static/lib/codemirror.js',
    fromTextArea=twc.js_function('CodeMirror.fromTextArea'),
)
codemirror_css = twc.CSSLink(
    modname=__name__,
    filename='static/lib/codemirror.css',
)

_codemirror_css = twc.CSSLink(
    modname=__name__,
    filename='static/style.css',
)

# codemirror_util_dir = twc.DirLink(
#     modname=__name__,
#     whole_dir=True,
#     filename='static/lib/util/',
# )

#TODO: Make addons programmatically usable
# codemirror_addons = dict(
#     (d, twc.DirLink(modname=__name__, filename=os.path.join('static/addon', d)))
#         for d in os.listdir(os.path.join(os.path.dirname(__file__), 'static/addon')))

codemirror_addons = {
    'display': {
        'placeholder': twc.JSLink(modname=__name__,
            filename='static/addon/display/placeholder.js',
            resources=[codemirror_js],
        ),
        'fullscreen': twc.JSLink(modname=__name__, filename='static/addon/display/fullscreen.js',
            resources=[twc.CSSLink(modname=__name__, filename='static/addon/display/fullscreen.css'), codemirror_js],
        ),
    },
    'mode': {
        'meta': twc.JSLink(modname=__name__, filename='static/mode/meta.js',
            resources=[codemirror_js],
        ),
    },
}

codemirror_keymaps = dict(
    (f.rstrip('.js'), twc.JSLink(modname=__name__, filename=os.path.join('static/keymap', f), resources=[codemirror_js]))
        for f in os.listdir(os.path.join(os.path.dirname(__file__), 'static/keymap')))

codemirror_modes = dict(
    (d, twc.JSLink(modname=__name__, filename=os.path.join('static/mode', d, d + '.js'), resources=[codemirror_js]))
        for d in os.listdir(os.path.join(os.path.dirname(__file__), 'static/mode')))

codemirror_themes = dict(
    (f.rstrip('.css'), twc.CSSLink(modname=__name__, filename=os.path.join('static/theme', f), resources=[codemirror_js]))
        for f in os.listdir(os.path.join(os.path.dirname(__file__), 'static/theme')))


def mode_name(mode):
    '''Tries best-effortly to get the right mode name'''

    if mode:
        l = mode.lower()

        if l in ('java', ):
            return ('clike', 'text/x-java')
        if l in ('c', ):
            return ('clike', 'text/x-csrc')
        if l in ('c++', 'cxx'):
            return ('clike', 'text/x-c++src')
        if l in ('csharp', 'c#'):
            return ('clike', 'text/x-csharp')

        if l in ('sh', 'bash', ):
            return ('shell', 'text/x-sh')

        if l in codemirror_modes:
            return (l, None)

    return (None, None)


class CodeMirrorEditor(twf.TextArea):
    # declare static resources here
    resources = [codemirror_js, codemirror_css, _codemirror_css]

    mode = twc.Param('The highlighting mode for CodeMirror', default=None)
    keymap = twc.Param('The keymap for CodeMirror', default=None)
    theme = twc.Param('The theme for CodeMirror', default=None)

    fullscreen = twc.Param('Whether to include the fullscreen editing addon', default=False)
    height_from_rows = twc.Param('Whether to set the CodeMirror height from the rows', default=True)

    lineNumbers = twc.Param(default=True)
    firstLineNumber = twc.Param(default=None)

    options = twc.Param('Additional CodeMirror configuration options, '
            'see http://codemirror.net/doc/manual.html#config for more info',
        default=None)
    default_options = {
        # 'theme': 'default',
        # 'keymap': 'default',
        'indentUnit': 4,
        'lineWrapping': True,
        'autofocus': False,
    }

    # @classmethod
    # def post_define(cls):
    #     pass
    #     # put custom initialisation code here

    def prepare(self):
        # put code here to run just before the widget is displayed
        super(CodeMirrorEditor, self).prepare()
        self.safe_modify('resources')

        options = self.default_options.copy()
        if self.options:
            options.update(self.options)

        try:
            (mode, mime) = mode_name(self.mode)
            self.resources.append(codemirror_modes[mode])
            options['mode'] = mime or mode
        except KeyError:
            pass

        if self.keymap:
            try:
                self.resources.append(codemirror_keymaps[self.keymap])
                options['keymap'] = self.keymap
            except KeyError:
                pass

        if self.theme:
            try:
                self.resources.append(codemirror_themes[self.theme])
                options['theme'] = self.theme
            except KeyError:
                pass

        options['lineNumbers'] = bool(self.lineNumbers)

        if self.firstLineNumber:
            options['firstLineNumber'] = self.firstLineNumber

        if self.height_from_rows and self.rows is not None:
            _css = twc.CSSSource(src=u'#%s + .CodeMirror {height: %dem;}' % (self.compound_id, self.rows))
            self.resources.append(_css)

        if self.fullscreen:
            self.resources.append(codemirror_addons['display']['fullscreen'])
            #TODO: Customizable keys
            self.default_options['extraKeys'] = {
                "F11": twc.js_callback('function(cm) {cm.setOption("fullScreen", !cm.getOption("fullScreen"));}'),
                "Esc": twc.js_callback('function(cm) {if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);}'),
            }
            try:
                _help_text = self.help_text
            except AttributeError:
                _help_text = u''
            self.safe_modify('help_text')
            self.help_text = 'Press F11 when cursor is in the editor to toggle full screen editing. ' \
                             'Esc can also be used to exit full screen editing.' \
                             + Markup('<br />') + (_help_text if _help_text else '')

        if self.placeholder:
            self.resources.append(codemirror_addons['display']['placeholder'])

        self.add_call(codemirror_js.fromTextArea(twc.js_function('document.getElementById')(self.compound_id),
                                                 options))


class CodeMirrorDisplay(CodeMirrorEditor):
    '''A CodeMirror widget for displaying and highlighting a snippet of code

    This instance will be read-only, of course.
    To achieve dynamic sizing in height, rows should not be set.
    '''

    css_class = 'CodeMirrorDisplay'

    @classmethod
    def post_define(cls):
        cls.default_options = cls.default_options.copy()
        cls.default_options.update({'readOnly': 'nocursor', 'viewportMargin': twc.js_symbol('Infinity')})
