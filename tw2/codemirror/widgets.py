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


class CodeMirrorWidget(twf.TextArea):
#    template = "tw2.codemirror.templates.codemirror"

    # declare static resources here
    # you can remove either or both of these, if not needed
    resources = [_codemirror_css, codemirror_css, codemirror_js]

    mode = twc.Param('The highlighting mode for CodeMirror', default=None)
    theme = twc.Param('The theme for CodeMirror', default=None)
    lineNumbers = twc.Param(default=True)

    @classmethod
    def post_define(cls):
        pass
        # put custom initialisation code here

    def prepare(self):
        super(CodeMirrorWidget, self).prepare()
        # put code here to run just before the widget is displayed
        if self.mode:
            self.resources.append(codemirror_modes[self.mode])
        if self.theme:
            self.resources.append(codemirror_themes[self.theme])
        self.add_call(
            codemirror_js.fromTextArea(twc.js_function('document.getElementById')(self.compound_id), {
                'lineNumbers': self.lineNumbers,
                }))
