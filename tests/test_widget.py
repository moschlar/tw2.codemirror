from tw2.core.testbase import WidgetTest
from tw2.codemirror import *

class TestCodemirror(WidgetTest):
    # place your widget at the TestWidget attribute
    widget = Codemirror
    # Initilization args. go here 
    attrs = {'id':'codemirror-test'}
    params = {}
    expected = """<div id="codemirror-test"></div>"""
