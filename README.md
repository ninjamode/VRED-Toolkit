# VRED-Toolkit

VRED tools for a improved virtual reality experience. Comes with a tool loader system that allows you to easily extend VRED and develop your own tools. Tool code will be embedded into the current scene as a Variant Set and are saved together with the scene.



## Installation

Add this folder to ~/Documents/Autodesk/VRED-_VRED-Version_/ScriptPlugins/

You might need to create the VRED-_VRED-Version_ and ScriptPlugins folders.



## Usage

Use the new `VR Tools` menu in VRED to add tools to the current scene. Tools will be injected as variants, adjustable tool setup code will be added to the script editor.



## Caveats

Upon injecting a tool, the current filename and path will be lost and replaced by a temporary file location. Make sure you save your file with the proper filename again. Later usage of a tool will not change the filename.

These scripts are examples of how VRED can be extended, and might break things. Use with caution. Autodesk does not support these extensions. I might or might not be able to fix problems in these scripts.



## Developing your own tools

Tools for this toolkit consist of one main file, and need to be placed in the "tools" directory (where already tools like paint or screenshot are).

_Important_: Tool files should consist of valid Python code only, but must be saved without any file extension! This is to prevent VRED from trying to automatically execute this plugins code at every launch and creating a menu entry under "Scripts".

The complete files content will be added to the current scene as a VariantSet. The files `_editor_code` variable content will be appended to the current editor script. Place any setup code for your plugin here (like executing the VariantSet with the actual plugin code).

The `_file` variable can point to an `.osb` file, which will be added to the current scene together with the code. This allows you to ship custom geometry and materials with your plugin. Set to `None` if you don't want to load any files.



## Tools

__Vive Advanced Teleport__: Script to teleport within a virtual reality scene using vive touch controllers. Can be used to jump to a location or pre configured jump points. See https://knowledge.autodesk.com/support/vred-products/learn-explore/caas/simplecontent/content/advanced-teleport-for-the-htc-vive-any-vred-scene.html for more information and example scenes.

Options include: 

`ball_mat` jump point material

`ball_highlight_mat` selected jump point material

`jump_min_dist` minimum distance from a jump point in mm for it to be displayed (default = 4000)

`tp_name` Jump point node name start string, eg. TelePort_1 (default = "TelePort")

`ground_name` Walkable object name starting string, eg. Ground_1, Ground_floor2 (default = "Ground").

`ground_tag` Nodes with this string as a tag will also be treated as walkable objects (default = "_toolkit_tp_ground")

`ground_list` Additional list of walkable objects (vrNodePtr). Supply generated lists of walkable nodes here.

`show_tp_axis` Show or hide the green teleport direction ray (default = True)

`through_geometry` Allow teleportation through geometry. Can be laggy in complex scenes. (default = False)

`exclude_tag` Node with this tag will be not block teleportation (default = "_toolkit_tp_exclude")

`exclude_list` Allow teleportation through nodes in this list (vrnodePtr). More granular alternative to `through_geometry`. Previously walkable geometry in this list will no longer be walkable.



You can only teleport onto surfaces with either their name starting with `ground_name` or with the `ground_tag`. This script defaults to teleporting with the trigger button. You can use the touchpad button to interactively assign the ground tag to geometry to make it walkable. Make sure you do not change the cameras position or rotation while in VR; The camera needs to be at origin.

Teleport jump points support 4 modes of operation:

- Keep head rotation and only adjust player position
- Adjust tracking space rotation and player position. This will result in random player view direction, based on the current view direction. Use this to e.g. rotate the tracking space to fit in a room or reset it.
- Adjust player view direction and position. Players will always look in the specified direction. This corrects for hmd rotation (results in a rotated tracking space)
- Adjust player view direction, position and height. Players will always look in the specified direction. This will additionally camera height (__z__ axis) to the specified point (regardless of physical player height). Height will be reset after the next teleport.

Jump points will never change players __x__ or __y__ axis head rotation.



---

__screenshot__: Creates a screenshot of your current viewport. Files will be named after the current scene name.

`path` Where to save the screenshots (default = Desktop)



---

__paint__: Allows you to draw into any VRED scene in VR using your controller. Uses a pooling system with path elements for smooth performance even in big scenes. Stroke color can be dynamically change with the touchpad while painting.

__IMPORTANT__: Currently does not work for extended periods of time, as constraints can not be deleted in VRED 2018.4 and earlier. The longer you draw, the more CPU your scene will use. Future versions of VRED might fix this problem.

`pool_size`: Number of paint stroke pieces in the pool. More pieces create cpu and gpu overhead, but allow for longer paint strokes. Can be changed dynamically.

`min_dist`: Distance to the last stoke after which a new element will be placed. Smaller numbers create smoother looking stroke, but shorten it overall.

`offset`: Extra stroke part length. balance between holes and coarse look. 0.1 is a good default value, you probably don't need to change this.

`stroke_width`: Width of the paint stroke.