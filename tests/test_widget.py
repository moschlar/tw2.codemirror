from tw2.core.testbase import WidgetTest
from tw2.codemirror import *


class TestCodemirror(WidgetTest):
    # place your widget at the TestWidget attribute
    widget = CodeMirrorWidget
    # Initialization args go here
    attrs = {'id': 'codemirror-test'}
    params = {}
    expected = """<textarea name="codemirror-test" id="codemirror-test"></textarea>"""
