#These Sample scripts are not supported under any Autodesk standard support program or service.
#The sample scripts are provided without warranty of any kind.
#Autodesk disclaims all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for a particular purpose.
#The entire risk arising out of the use or performance of the sample scripts and documentation remains with you.

from PySide2 import QtWidgets
from PySide2 import QtCore
import vrController, vrVariantSets, vrFileIO
import os    
import tempfile
import shutil
import imp


def plugin_path():
    version = vrController.getVredVersion()
    path = os.path.join(os.path.expanduser('~'), "Documents", "Autodesk", "VRED-" + version, "ScriptPlugins", "VRED-Toolkit")
    return path


def vredMainWindow(id):
    from shiboken2 import wrapInstance
    return wrapInstance(id, QtWidgets.QMainWindow)


def inject_script_variant(name, script):
    vset = vrVariantSets.createVariantSet(name)
    vset.addScript(script)


def add_tool(name, code, script_ext = None, file = None):
    '''
    Adds a tool the current scene.
    Injects a Variantset with tool code, and extends the script editor
    with some setup code.
    Only injects if a Variantsame with the tool name does not already 
    exist, otherwise it's assumed the tool is loaded
    '''
    
    # Bail if stuff is already loaded
    if "VRTools_{}".format(name) in vrVariantSets.getVariantSets():
        return

    inject_script_variant("VRTools_{}".format(name), code)

    if file:
        vrFileIO.load(os.path.join(plugin_path(), file))

    # Hacky way to extend the editor script
    if script_ext:
        tempdir = tempfile.mkdtemp()
        filepath = os.path.join(tempdir, "scripts.py")
        vrFileIO.save(filepath)
        with open(filepath, 'a') as scripts_file:
            scripts_file.write(script_ext)
        vrFileIO.load(filepath)
        shutil.rmtree(tempdir)


def add_vrtools_menu():
    ''' Find all tools in the tools folder, load them and create a menu entry '''
    mw = vredMainWindow(VREDMainWindowId)
    menu = QtWidgets.QMenu(mw.tr("VR Tools"), mw)

    # find all tools
    for filename in os.listdir("tools"):
        tool_path = os.path.join("tools", filename)

        # Import tool to access file and editor code
        tool = imp.load_source(filename, tool_path)

        # Read tool file for vset injection
        with open(tool_path, 'r') as tool_file:
            tool_code = tool_file.read()

        action = QtWidgets.QAction(mw.tr("Add {}".format(filename)), mw)
        action.triggered.connect(
            lambda name=filename, tool_code=tool_code, editor_code=tool._editor_code, file=tool._file:
            add_tool(name, tool_code, editor_code, file))
        menu.addAction(action)
        print "Added {} tool".format(filename)


    # insert VR Toolkit menu before Help.
    actions = mw.menuBar().actions()
    for action in actions:
        if action.text() == mw.tr("&Help"):
            mw.menuBar().insertAction(action, menu.menuAction())
            break

add_vrtools_menu()


# Script created by Constantin Kleinbeck, supported by Simon Nagel