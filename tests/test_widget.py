from tw2.core.testbase import WidgetTest
from tw2.codemirror import *


class TestCodeMirrorEditor(WidgetTest):
    # place your widget at the TestWidget attribute
    widget = CodeMirrorEditor
    # Initialization args go here
    attrs = {'id': 'codemirror-test'}
    params = {}
    expected = """<textarea name="codemirror-test" id="codemirror-test"></textarea>"""


class TestCodeMirrorDisplay(WidgetTest):
    # place your widget at the TestWidget attribute
    widget = CodeMirrorDisplay
    # Initialization args go here
    attrs = {'id': 'codemirror-test'}
    params = {}
    expected = """<textarea name="codemirror-test" id="codemirror-test" class="CodeMirrorDisplay"></textarea>"""
