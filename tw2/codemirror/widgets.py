import tw2.core as twc


class Codemirror(twc.Widget):
    template = "genshi:tw2.codemirror.templates.codemirror"

    # declare static resources here
    # you can remove either or both of these, if not needed
    resources = [
        twc.JSLink(modname=__name__, filename='static/codemirror.js'),
        twc.CSSLink(modname=__name__, filename='static/codemirror.css'),
    ]

    @classmethod
    def post_define(cls):
        pass
        # put custom initialisation code here

    def prepare(self):
        super(Codemirror, self).prepare()
        # put code here to run just before the widget is displayed
