# OUT Null Creator v1.0
A simple script to rename, recolor and reshape your OUT nulls. Setup your preferences using the UI window (First launch only). Create a corresponding object merge as a bonus!

Tool Description:
1. Asks for User Preferences (first launch only) and saves it into a text file in User Documents folder.
2. Modifies an exisiting selected null based on saved User Preferences.
3. If selected node is not a null, Creates an OUT Null and connects to last selected node based on saved User Preferences.

>[!note]
>The setup process for this script in Houdini is explained further down in this readme file. 

## UI Preview

When the script is run for the first time, you can setup your preferences for auto-adding a prefix to the node name, color of the nodes and the shape for the null node and object merge node.
<p align="middle">
  <img src="https://github.com/user-attachments/assets/0ecc4449-61ec-4a60-91a8-d09d95ff81b7" width = 300 />
</p> 

Once the preferences are saved, you can start modifying or creating nulls and object merges and it will do this based on your user preferences.

<p align="middle">
  <img src="https://github.com/user-attachments/assets/9eb08d01-ced0-49a6-868b-52ccbb457637" width="353" />
  <img src="https://github.com/user-attachments/assets/79ec5d39-e0af-4c33-99bc-2dd4bcf8a349" width="279" />
  <img src="https://github.com/user-attachments/assets/85320833-fbc1-431f-a667-5aa9ad18ac86" width="266" />
</p>

## Tool Setup and Demo

This section goes through the initial setup of this tool and showcases it's tested use-cases.

---

### Setting up the shelf tool and configuring hotkey to call the script

To get started:
1. On your shelf tools tab, create a new shelf tool.
2. Set the Name to OUT_Null_Creator_v1.0 and the Label to OUT Null Creator v1.0.
3. Copy the code in [OUT Null Creator v1.0.py](https://github.com/surajvfx/OUTNullCreator/blob/f10ede9a8f786c4510dc1a28fab7ab6afb2d65ed/Out%20Null%20Creator%20v1.0.py) and paste it in the script tab of the new tool dialog box.
4. Finally, under hotkeys - edit the Network Pane hotkeys and set it to your chosen shortcut to call the script.

>[!tip]
> You can use Numpad 0 key or the back-tick (`) key as a hot key to call this script!

Here's a quick setup guide:
<p align="middle">
  <img src="https://github.com/user-attachments/assets/15e448e9-442d-4c04-987b-f91fdcad4da9" width="700" />
</p>

---

### Running the script for the first time

- When you run this script for the first time, the user preferences UI window should pop-up.
- You can select the color for the nodes, set a prefix for the null nodes that get created or modified by the script.
- You can also set node shapes for the null nodes and object merge nodes individually.

>[!tip]
>The node shape names correspond to the node shape menu in the network bar (Z key). You can use that for reference.

Here's a quick UI setup guide and tool demo:
<p align="middle">
  <img src="https://github.com/user-attachments/assets/2515a6e3-8372-434b-922a-f510f79f55bc" width="700" />
</p>

>[!note]
>You only need to set this up once. To change your preferences in the future, simply delete the "outNullUserPref.txt" in your documents folder and re-run this script.

---

>[!Caution]
> - This tool is only designed to run in the geometry/ SOP context and hasn't been tested for other houdini contexts.
> - A node needs to be selected before running this script. You will be greeted with a info dialog asking you to do so.
