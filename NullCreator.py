"""
Tool Name: Out Null Creator v1.0
Author: Suraj Bathija
Tool Description: 1. Asks for User Preferences (first launch only) and saves it into a text file.
                  2. Creates an OUT Null on last selected node if it's not a Null Node based on saved User Preferences.
                  3. Modifies an exisiting selected null based on saved User Preferences.

Note: Preferences are saved in User folder as a .txt file and can be deleted to re-save new user prefs

Suggestion: Under Hotkeys, Set Network Pane Shortcut to numpad 0 or any other available shorcut key
            for quick access to the tool
"""
import hou
import os
import time
from PySide2 import QtGui, QtWidgets, QtCore

# Define Global Variables
global prefs
global shapes

# Define file paths
usr = str(os.path.expanduser("~"))
docs = (usr+"/Documents")
txt = str('outNullUserPref.txt')
prefs = docs+"/"+txt

# Get Node Shapes and store them into shapes global variable
editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
shapes = editor.nodeShapes()

# Define Class MainWindow as QWidget which will hold all UI
class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Out Null Creator v1.0")
        self.setMaximumSize(400, 800)
 
        # Create vertical box layout for window
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(10)
        layout.setMargin(15)
        self.setLayout(layout) 
        
        # Group Box to select color from a pallette and add widget to window layout 
        self.color_box = QtWidgets.QGroupBox("Select Color", self)
        self.color_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self.color_box)
        
        # Create horizontal box widget layout which contains color palette
        color_layout = QtWidgets.QHBoxLayout()
        self.color_box.setLayout(color_layout)

        # Create color palette and add widget to color layout
        self.palette = hou.qt.ColorPalette(size=64,columns=4, rows=4)
        self.palette.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        color_layout.addWidget(self.palette)
        self.palette.colorSelected.connect(self.chosen_color)
        
        # Group box to add a prefix and add widget to window layout
        self.prefix_box = QtWidgets.QGroupBox("Add Prefix", self)
        self.prefix_box.setCheckable(True)
        self.prefix_box.setChecked(0)
        self.prefix_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self.prefix_box)
        self.prefix_box.toggled.connect(self.prefix_value)
        
        # Create horizontal box widget layout which contains prefix
        prefix_layout = QtWidgets.QVBoxLayout()
        prefix_layout.setSpacing(10)
        self.prefix_box.setLayout(prefix_layout)
        
        # Create QLineEdit to take user input for Prefix
        self.name_prefix = QtWidgets.QLineEdit()
        self.name_prefix.setMinimumSize(80,30)
        prefix_layout.addWidget(self.name_prefix)
        self.name_prefix.setText("OUT_")
        
        # Check Box for enabling popup for name input
        self.renameCheck = QtWidgets.QCheckBox("Show Rename Dialog Box Everytime", self)
        self.renameCheck.setChecked(0)
        prefix_layout.addWidget(self.renameCheck)
        self.renameCheck.stateChanged.connect(self.renameCheck_status)
        
        # Group box for selecting a shape for Null and add widget to window layout
        self.null_shape_box = QtWidgets.QGroupBox("Select Null Shape", self)
        self.null_shape_box.setCheckable(False)
        self.null_shape_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self.null_shape_box)
        
        # Create horizontal box widget layout which contains null shape combo box        
        null_box_layout = QtWidgets.QHBoxLayout()
        self.null_shape_box.setLayout(null_box_layout)

        # Combo Box for Null shapes
        self.nullcomboBox = QtWidgets.QComboBox(self)
        self.nullcomboBox.setObjectName("comboBox")
        null_box_layout.addWidget(self.nullcomboBox)
        self.nullcomboBox.setMinimumSize(80,40)

        for shape in shapes:
            self.nullcomboBox.addItem(shape)
            
        self.nullcomboBox.setCurrentIndex(6)
        
        # Group Box for Object Merge checkbox and merge shapes combo box
        self.check_box = QtWidgets.QGroupBox("Select Object Merge Shape", self)
        self.check_box.setCheckable(False)
        self.check_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self.check_box)
        
        # Create vertical box widget layout which contains merge shape combo box and check box  
        merge_box_layout = QtWidgets.QVBoxLayout()
        merge_box_layout.setSpacing(10)
        self.check_box.setLayout(merge_box_layout)

        # Combo Box for Object Merge shapes
        self.mergeComboBox = QtWidgets.QComboBox(self)
        self.mergeComboBox.setObjectName("mergeBox")
        self.mergeComboBox.setMinimumSize(80,40)
        merge_box_layout.addWidget(self.mergeComboBox)

        for shape in shapes:
            self.mergeComboBox.addItem(shape)
            
        self.mergeComboBox.setCurrentIndex(7)
        self.mergeComboBox.setEnabled(False)
        
        global mergeBox
        mergeBox = self.mergeComboBox
        
        # Check Box for creating a corresponding Object Merge
        self.check = QtWidgets.QCheckBox("Create Corresponding Object Merge", self)
        self.check.setChecked(0)
        merge_box_layout.addWidget(self.check)
        self.check.stateChanged.connect(self.checkBox_status)
        
        # Create save button and add to window layout
        self.save_button = QtWidgets.QPushButton("Save preferences to File", self)
        self.save_button.setMinimumSize(80, 40)
        layout.addWidget(self.save_button)
        
        self.save_button.clicked.connect(self.savePrefs)
        self.save_button.clicked.connect(self.notifyUser)
    
        # Create save progress Bar and add to window layout
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
    # Declare global variable checkBoxState and initialise with value of 0    
    global renameCheckState    
    renameCheckState = str("0")
        
    # Check create merge checkbox and set state    
    def renameCheck_status(self, state):     
        
        global renameCheckState
        
        if state > 0:
            renameCheckState = str("1")
        else:
            renameCheckState = str("0")
    
    # Declare global variable checkBoxState and initialise with value of 0    
    global checkBoxState    
    checkBoxState = str("0")
        
    # Check create merge checkbox and set state    
    def checkBox_status(self, state):     
        
        global checkBoxState
        
        if state > 0:
            mergeBox.setEnabled(True)
            checkBoxState = str("1")
        else:
            mergeBox.setEnabled(False)
            checkBoxState = str("0")
    
    # Declare global variable colour and initialise with value             
    global colour
    colour = str("[64,64,64]")
    
    # Check the user selected color and save it      
    def chosen_color(self, ix, color):
        selectedColor = [color.red(), color.green(), color.blue()]
        global colour
        colour = str(selectedColor)
    
    # Update Progress bar when user presses save preferences button    
    def update_progress_bar(self):
        self.progress_bar.setValue(0)
        for i in range(101):
            self.progress_bar.setValue(i)
            time.sleep(0.001)  
            QtWidgets.QApplication.processEvents()  
    
    # Declare global variable prefix and initialise with no value         
    global prefix
    prefix = ""
    
    def prefix_value(self):
        global prefix
        prefix = str(self.name_prefix.text())       
    
    #Save preferences
    def savePrefs(self):
        global selected_shape
        null_shape = self.nullcomboBox.currentText()
        global merge_shape
        merge_shape = self.mergeComboBox.currentText()
        
        parms = (colour+"\n"
                 +prefix+"\n"
                 +null_shape+"\n"
                 +merge_shape+"\n"
                 +checkBoxState+"\n"
                 +renameCheckState+"\n"
                )       

        #write to text file
        file = open(prefs, 'w')
        file.write(parms)
        file.close()

        self.update_progress_bar()   
        self.close()
        
    def notifyUser(self):
        hou.ui.displayMessage("Preferences Saved in: %s" % prefs, buttons=("Ok",), close_choice = 1)
        
#Read saved preferences from file everytime this script is called
def read_prefs():
            
    file = open(prefs, 'r')
    content = file.read()
    file.close()
    
    list = str.split(content, "\n")
    global color
    global prefix
    global rounded_color
    global read_shape
    global read_merge_shape
    global int_state
    global read_renameCheck

    color = list[0]
    color = str.replace(color, "[", "")
    color = str.replace(color, "]", "")
    color = str.replace(color, " ", "")
    color = color.split(',')
    float_color = tuple(float(x) for x in color)
    divided_color = tuple(x/255 for x in float_color)
    rounded_color = tuple(round(x, 2) for x in divided_color) 
    prefix = list[1]
    read_shape = list[2]
    read_merge_shape = list[3]
    read_merge_state = list[4]
    read_renameCheck = list[5]
    int_state = int(read_merge_state)
    return(rounded_color)
    return(prefix)
    return(read_shape)
    return(read_merge_shape)
    return(int_state)
    return(read_renameCheck)

#Ask user to set node name and add the prefix to it    
def node_name():
    
    global final_name
    global user_name
    
    int_renameCheck = int(read_renameCheck)
    
    #check user preferences for rename node popup
    if int_renameCheck > 0:
        input_name = (hou.ui.readInput('Rename Node', buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title=None))
        if len(input_name[1]) > 1:
            user_name = str.replace(input_name[1], " ", "_")
        else:
            user_name = str("")
    else:
        user_name = str("")
        
    final_name = prefix + user_name    
    
    #check length of string final_name and assign a string value if it's empty
    if len(final_name) < 1:
        final_name = str("NULL")
   
    return(final_name)
    return(user_name)
    
#get selected nodes
select = hou.selectedNodes()

def createNull():

    global created_null

    #get last selected node and get the name as string
    node = select[-1]
    nodeName = str(node)
    
    #get the position of selected node and add -2 in y direction for new position
    position = node.position()
    addPos = hou.Vector2(0, -2)
    newPos = position + addPos

    #get the path of selected node as string and store parent path in newPath
    path = str(node.path())
    newPath = str.replace(path, nodeName, "")

    #create a null object in previously defined path
    null = hou.node(newPath).createNode("null")

    #generate name from parent node and apply to null with prefix
    newName = final_name
    
    #set name, color and shape
    null.setName(newName,unique_name=True)
    null.setColor(hou.Color(rounded_color))
    null.setUserData('nodeshape', read_shape)
    
    #set new postion in network view and set first input as selected node
    null.move(newPos)
    null.setFirstInput(node)
    hou.node(newPath).layoutChildren(items=(node, null), horizontal_spacing=+1.0, vertical_spacing=+2.0)

    created_null = newPath+newName
    return(created_null)

def modifyNull():

    global existing_null

    #get last selected node and get the name as string
    node = select[-1]
    
    #generate name from parent node and apply to null with prefix
    newName = final_name
    
    #set name, color and shape
    node.setName(newName,unique_name=True)
    node.setColor(hou.Color(rounded_color))
    node.setUserData('nodeshape', read_shape)

    #get the path of selected node as string and store parent path in newPath
    path = str(node.path())
    
    existing_null = path
    return(existing_null)
    
def createNullatCursor():

    global created_null
    global curPos
    
    #get the position of selected node and add -2 in y direction for new position
    curPos = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).cursorPosition()
    position = curPos

    #get the path of selected node as string and store parent path in newPath
    paneTabObj = hou.ui.paneTabUnderCursor()
    path = paneTabObj.pwd().path()

    #create a null object in previously defined path
    null = hou.node(path).createNode("null")
    null.move(curPos)

    #generate name from parent node and apply to null with prefix
    newName = final_name
    
    #set name, color and shape
    null.setName(newName,unique_name=True)
    null.setColor(hou.Color(rounded_color))
    null.setUserData('nodeshape', read_shape)

    created_null = path+"/"+newName
    return(created_null)
    
def createMerge():

    #check if nodes are selected, else create merge for null at cursor position
    if len(select) > 0:
        #get last selected node and get position, name as string
        node = select[-1]
        nodeName = str(node)
        position = node.position()
        #get the position of selected node and add values for new position
        type = node.type()
        if type == hou.sopNodeTypeCategory().nodeType("null"):
            addPos = hou.Vector2(0, -2)
        else:
            addPos = hou.Vector2(0, -4)
        newPos = position + addPos
        
        #get the path of selected node as string and store parent path in newPath
        path = str(node.path())
        newPath = str.replace(path, nodeName, "")
            
    else:
        #get cursor position, path and set position values
        curPos = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).cursorPosition()
        position = curPos
        paneTabObj = hou.ui.paneTabUnderCursor()
        path = paneTabObj.pwd().path()
        newPath = path
        addPos = hou.Vector2(0, -2)     
        newPos = position + addPos

    #create a merge object in previously defined path
    merge = hou.node(newPath).createNode("object_merge")
    
    #set merge parameter to user selected null or created null
    if len(select) > 0:
        node = select[-1]
        type = node.type()
        if type == hou.sopNodeTypeCategory().nodeType("null"):
            merge.parm('objpath1').set(existing_null)
        else:
            merge.parm('objpath1').set(created_null)
    else:
        merge.parm('objpath1').set(created_null)
        
    #generate name from user prefix+input and apply to merge with prefix
    newName = "MERGE_" + user_name
   
    #set name, color and shape
    merge.setName(newName,unique_name=True)
    merge.setColor(hou.Color(rounded_color))
    merge.setUserData('nodeshape', read_merge_shape)
    
    #set new postion in network view and set first input as selected node
    merge.move(newPos)

try:
    MainWindow.close()
    MainWindow.deleteLater()
except:
    pass

window = MainWindow()    

def runCommands():
    #Check if preferences .txt file exists; if not, open user prefs panel
    if os.path.isfile(prefs):
        file = open(prefs, 'r')
        content = file.read()
        file.close()
        list = str.split(content, "\n")
        #check if there are any selected nodes; if not, create null at cursor position
        if len(select)>0:
            node = select[0] 
            type = node.type()
            #Check if preferences file is not empty
            if len(list[0])>0:
                read_prefs()
                time.sleep(0.1)
                #check if selected node type is a null
                if type == hou.sopNodeTypeCategory().nodeType("null"):
                    node_name()
                    modifyNull()
                else:
                    node_name()
                    createNull()
                #check if user preferences has state 1 for create merge
                if int_state > 0:
                    createMerge()  
            else:
                time.sleep(0.5)
                window.show()      
        else:
            read_prefs()
            node_name()
            createNullatCursor()
            if int_state > 0:
                createMerge()
    else:
        time.sleep(0.5)
        window.show()    
        
runCommands()
