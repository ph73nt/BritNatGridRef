BritNatGridRef - the readme file!

Overview
--------

BritNatGridRef is a plugin written in Python for the QGIS geographic 
information system (www.qgis.org). The latest version of BritnatGridRef can be 
found at the Github repository (https://github.com/ph73nt/BritNatGridRef or 
simply search for BritNatGridref).

The plugin is to add a point of interest to an existing and active vector 
layer. The user enters the grid reference of the point and then any optional 
attributes to add to the feature (mulitple features are allowed, separated by 
commas). To use the attributes, it should be noted that the active layer must 
already be able to accept attributes (configurable in the "Attribute table" of 
the active layer).

Usage
-----

Install the plugin in the usual location specified in the QGIS documentation. 
The plugin is then available for the plugins menu: 

Plugins > BritNatGridRef > BritNatGridRef

The user is shown a simple dialogue with text fields for the British Nation 
Grid reference point and a second text field for optional attributes. the user 
fills in the fields and presses enter (or clicks OK). 

Errors and complications
------------------------

Several pitfalls are trapped by the plugin (for instance an incorrect grid 
reference), but is by no means foolproof. Errors, bugs and feature requests 
should be added to the Github page:

https://github.com/ph73nt/BritNatGridRef/issues

or alternatively contact the author by email: njt@fishlegs.co.uk