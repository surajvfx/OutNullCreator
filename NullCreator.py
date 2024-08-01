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
prefs = docs+"\\"+txt

# Get Node Shapes and store them into shapes global variable
editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
shapes = editor.nodeShapes()

# Define Class MainWindow as QWidget which will hold all UI
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Out Null Creator v1.0")
 
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(10)
        layout.setMargin(15)
        self.setLayout(layout)
        
        # Group Box to select color from a pallette
        self.color_box = QtWidgets.QGroupBox("Select Color", self)
        self.color_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        color_layout = QtWidgets.QHBoxLayout()
        self.color_box.setLayout(color_layout)
        layout.addWidget(self.color_box)

        self.palette = hou.qt.ColorPalette(size=64,columns=4, rows=4)
        self.palette.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        color_layout.addWidget(self.palette)
        self.palette.colorSelected.connect(self.chosen_color)
        
        # Group box to add a prefix
        self.group_box = QtWidgets.QGroupBox("Add Prefix", self)
        self.group_box.setCheckable(True)
        layout.addWidget(self.group_box)
        
        group_layout = QtWidgets.QHBoxLayout()
        self.group_box.setLayout(group_layout)
        self.name_prefix = QtWidgets.QLineEdit()
        self.name_prefix.setMinimumSize(80,30)
        group_layout.addWidget(self.name_prefix,stretch=3)
        self.name_prefix.setText("OUT_")
        
        # Group box for selecting a shape for Null
        self.shape_box = QtWidgets.QGroupBox("Select Null Shape", self)
        self.shape_box.setCheckable(False)
        
        shapebox_layout = QtWidgets.QHBoxLayout()
        self.shape_box.setLayout(shapebox_layout)
        layout.addWidget(self.shape_box)

        # Combo Box for Null shapes
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setObjectName("comboBox")
        shapebox_layout.addWidget(self.comboBox)
        self.comboBox.setMinimumSize(80,40)

        for shape in shapes:
            self.comboBox.addItem(shape)
            
        self.comboBox.setCurrentIndex(6)

        #Combo Box for Object Merge shapes
        merge_layout = QtWidgets.QVBoxLayout()
        merge_layout.setSpacing(10)
        
        self.mergeBox = QtWidgets.QComboBox(self)
        self.mergeBox.setObjectName("mergeBox")
        self.mergeBox.setMinimumSize(80,40)
        merge_layout.addWidget(self.mergeBox)

        for shape in shapes:
            self.mergeBox.addItem(shape)
            
        self.mergeBox.setCurrentIndex(7)
        self.mergeBox.setEnabled(False)
        
        global mergeBox
        mergeBox = self.mergeBox
        
        #Check Box for creating a corresponding Object Merge
        
        self.check_box = QtWidgets.QGroupBox("Select Object Merge Shape", self)
        self.check_box.setCheckable(False)
        
        self.check_box.setLayout(merge_layout)
        layout.addWidget(self.check_box)
           
        self.check = QtWidgets.QCheckBox("Create Corresponding Object Merge", self)
        self.check.stateChanged.connect(self.checkBox_status)
        merge_layout.addWidget(self.check)

        # Button Transference
        self.transfer_button = QtWidgets.QPushButton("Save preferences to File", self)
        self.transfer_button.setMinimumSize(80, 40)
        self.transfer_button.clicked.connect(self.savePrefs)
        self.transfer_button.clicked.connect(self.notifyUser)
        layout.addWidget(self.transfer_button)
    
        # Progress Bar
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
    # Check create merge checkbox and set state    
    def checkBox_status(self, state):
        global checkBoxState
        checkBoxState = str(state)
        
        if state > 0:
            mergeBox.setEnabled(True)
        else:
            mergeBox.setEnabled(False)
    
    # Check the user selected color and save it      
    def chosen_color(self, ix, color):
        selectedColor = [color.red(), color.green(), color.blue()]
        global colour
        colour = str(selectedColor)
    
    # Update Progress bar based when user presses save preferences button    
    def update_progress_bar(self):
        self.progress_bar.setValue(0)
        for i in range(101):
            self.progress_bar.setValue(i)
            time.sleep(0.001)  
            QtWidgets.QApplication.processEvents()  
      
    #Save preferences
    def savePrefs(self):
        
        prefix = str(self.name_prefix.text())
        global selected_shape
        selected_shape = self.comboBox.currentText()
        global merge_shape
        merge_shape = self.mergeBox.currentText()

        #write to text file
        file = open(prefs, 'w')
        file.write(colour+"\n")
        file.write(prefix+"\n")
        file.write(selected_shape+"\n")
        file.write(merge_shape+"\n")
        file.write(checkBoxState+"\n")
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
    int_state = int(read_merge_state)
    return(rounded_color)
    return(prefix)
    return(read_shape)
    return(read_merge_shape)
    return(int_state)

#Ask user to set node name and add the prefix to it    
def node_name():
    
    global final_name
    global user_name
    
    input_name = (hou.ui.readInput('Rename Node', buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=-1, help=None, title=None))
    user_name = str.replace(input_name[1], " ", "_")
    final_name = prefix + user_name
    return(final_name)
    return(user_name)
    print(final_name)
    print(user_name)
    
#get last selected node
select = hou.selectedNodes()

def createNull():

    global created_null

    #get first selected node and get the name as string
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

    #get first selected node and get the name as string
    node = select[0]
    
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
    
def createMerge():

    #get first selected node and get the name as string
    node = select[-1]
    nodeName = str(node)
    
    #get the position of selected node and add -2 in y direction for new position
    position = node.position()
    type = node.type()
    if type == hou.sopNodeTypeCategory().nodeType("null"):
        addPos = hou.Vector2(0, -2)
    else:
        addPos = hou.Vector2(0, -4)
    newPos = position + addPos

    #get the path of selected node as string and store parent path in newPath
    path = str(node.path())
    newPath = str.replace(path, nodeName, "")

    #create a merge object in previously defined path
    merge = hou.node(newPath).createNode("object_merge")

    #set merge parameter to user selected null
    if type == hou.sopNodeTypeCategory().nodeType("null"):
        merge.parm('objpath1').set(existing_null)
    else:
        merge.parm('objpath1').set(created_null)

    #generate name from parent node and apply to merge with prefix
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
    #check if there are any selected nodes; if not, notify user
    if len(select)>0:
        node = select[0] 
        type = node.type()
        #Check if preferences .txt file exists; if not, open user prefs panel
        if os.path.isfile(prefs):
            file = open(prefs, 'r')
            content = file.read()
            file.close()
            list = str.split(content, "\n")
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
            time.sleep(0.5)
            window.show()          
    else:
        hou.ui.displayMessage("No Nodes Selected", buttons=("Ok",), close_choice = 1)
        
runCommands()
