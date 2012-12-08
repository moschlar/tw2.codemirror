import os
import tw2.core as twc
import tw2.forms as twf


codemirror_js = twc.JSLink(
    modname=__name__,
    filename='static/lib/codemirror.js',
    fromTextArea=twc.js_function('CodeMirror.fromTextArea')
    )
codemirror_util_dir = twc.DirLink(
    modname=__name__,
    whole_dir=True,
    filename='static/lib/util/',
    )
codemirror_css = twc.CSSLink(
    modname=__name__,
    filename='static/lib/codemirror.css',
    )
_codemirror_css = twc.CSSSource(src=u'''
.CodeMirror {
    border: 1px solid black;
    background: #FFFFFF;
    width: 600px;
}
.CodeMirror-scroll {
    height: 200px;
}
''')

codemirror_keymaps = dict(
    (f.rstrip('.js'), twc.JSLink(modname=__name__, filename=os.path.join('static/keymap', f)))
    for f in os.listdir(os.path.join(os.path.dirname(__file__), 'static/keymap')))
codemirror_modes = dict(
    (d, twc.JSLink(modname=__name__, filename=os.path.join('static/mode', d, d + '.js')))
    for d in os.listdir(os.path.join(os.path.dirname(__file__), 'static/mode')))
codemirror_themes = dict(
    (f.rstrip('.css'), twc.CSSLink(modname=__name__, filename=os.path.join('static/theme', f)))
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


class CodeMirrorWidget(twf.TextArea):
#    template = "tw2.codemirror.templates.codemirror"

    # declare static resources here
    # you can remove either or both of these, if not needed
    resources = [codemirror_js, codemirror_css, _codemirror_css]

    mode = twc.Param('The highlighting mode for CodeMirror', default=None)
    theme = twc.Param('The theme for CodeMirror', default=None)
    options = twc.Param('CodeMirror configuration options, '
        + 'see http://codemirror.net/doc/manual.html#config for description',
        default={})
    default_options = {
        'theme': 'default',
        'indentUnit': 4,
        'lineNumbers': True,
        }

    @classmethod
    def post_define(cls):
        pass
        # put custom initialisation code here

    def prepare(self):
        super(CodeMirrorWidget, self).prepare()
        # put code here to run just before the widget is displayed
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

        try:
            self.resources.append(codemirror_themes[self.theme])
            options['theme'] = self.theme
        except KeyError:
            pass

        self.add_call(codemirror_js.fromTextArea(twc.js_function('document.getElementById')(self.compound_id), options))
