# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BritNatGridRef
                                 A QGIS plugin
 Plugin to add a point feature at a British National Grid Reference
                              -------------------
        begin                : 2015-04-09
        copyright            : (C) 2015 by Neil
        email                : njt@fishlegs.co.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import csv
import os.path
from qgis._core import QgsFeature, QgsGeometry, QgsPoint
from qgis.gui import QgsMessageBar
import qgis.utils

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon

from BritNatGridRef_dialog import BritNatGridRefDialog

class BritNatGridRef:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'BritNatGridRef_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = BritNatGridRefDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&BritNatGridRef')
        self.toolbar = self.iface.addToolBar(u'BritNatGridRef')
        self.toolbar.setObjectName(u'BritNatGridRef')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('BritNatGridRef', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/BritNatGridRef/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'BritNatGridRef'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&BritNatGridRef'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        # Stay open if required
        self.stayOpen = True
        while (self.stayOpen):
            # show the dialog
            self.dlg.show()
            # Run the dialog event loop
            result = self.dlg.exec_()
            # See if OK was pressed
            if result:
                
                # Check if dialogue should stay open
                self.stayOpen = self.dlg.addMore.isChecked()
                
                # Prep error messages
                msgBadGrid = "Sorry, I could not process the request; incorrect grid reference format"
                msgNoLayer = "Sorry, an error occurred - check there is a writable active layer"
              
                # Make hashtable of eastings and northings by grid reference
                east = {'HP':'4', 'HT':'3', 'HU':'4', 'HW':'1', 'HX':'2', 'HY':'3', 'HZ':'4', 'NA':'0', 'NB':'1', 'NC':'2', 'ND':'3', 'NF':'0', 'NG':'1', 'NH':'2', 'NJ':'3', 'NK':'4', 'NL':'0', 'NM':'1', 'NN':'2', 'NO':'3', 'NR':'1', 'NS':'2', 'NT':'3', 'NU':'4', 'NW':'1', 'NX':'2', 'NY':'3', 'NZ':'4', 'OV':'5', 'SC':'2', 'SD':'3', 'SE':'4', 'SH':'2', 'SJ':'3', 'SK':'4', 'SM':'1', 'SN':'2', 'SO':'3', 'SP':'4', 'SR':'1', 'SS':'2', 'ST':'3', 'SU':'4', 'SV':'0', 'SW':'1', 'SX':'2', 'SY':'3', 'SZ':'4', 'TA':'5', 'TF':'5', 'TG':'6', 'TL':'5', 'TM':'6', 'TQ':'5', 'TR':'6', 'TV':'5'}
                north = {'HP':'12', 'HT':'11', 'HU':'11', 'HW':'10', 'HX':'10', 'HY':'10', 'HZ':'10', 'NA':'9', 'NB':'9', 'NC':'9', 'ND':'9', 'NF':'8', 'NG':'8', 'NH':'8', 'NJ':'8', 'NK':'8', 'NL':'7', 'NM':'7', 'NN':'7', 'NO':'7', 'NR':'6', 'NS':'6', 'NT':'6', 'NU':'6', 'NW':'5', 'NX':'5', 'NY':'5', 'NZ':'5', 'OV':'5', 'SC':'4', 'SD':'4', 'SE':'4', 'SH':'3', 'SJ':'3', 'SK':'3', 'SM':'2', 'SN':'2', 'SO':'2', 'SP':'2', 'SR':'1', 'SS':'1', 'ST':'1', 'SU':'1', 'SV':'0', 'SW':'0', 'SX':'0', 'SY':'0', 'SZ':'0', 'TA':'4', 'TF':'3', 'TG':'3', 'TL':'2', 'TM':'2', 'TQ':'1', 'TR':'1', 'TV':'0'}  
        
                # Check for a match
                ref = self.dlg.textGridRef.text()
                
                refLen = len(ref)
                if refLen > 3:
                    
                    code = ref[0:2].upper()
                    print code
                        
                    # Check hashtable actually returns something
                    try:
                        e = east[code]
                        n = north[code]
                        print "East: ", e, " North: ", n
                
                        # Should now have the northings and eastings values... now need to add some more precision
                        metres = ref[2:]
                        l = len(metres)
                        print l
                        if l & 0x1:
                            # bad news, shouldn't have an odd number of digits... bomb out!
                            qgis.utils.iface.messageBar().pushMessage("Error", msgBadGrid, level=QgsMessageBar.CRITICAL)
                        else:
                            # Good news so far... even number of digits... split 'em in half and pad with zeroes
                            l /= 2
                            eMetres = metres[0:l]
                            while len(eMetres) < 5:
                                eMetres = eMetres + "0"
                
                            nMetres = metres[l:]
                            while len(nMetres) < 5:
                                nMetres = nMetres + "0"
                          
                            # Add the metres onto the eastings and northings
                            e += eMetres
                            n += nMetres
                            print e
                            print n
                        
                            # Great... now have out coordinates in QGIS acceptable format... add a new point
                        
                            # Get active layer
                            layer = qgis.utils.iface.activeLayer()
                          
                            caps = layer.dataProvider().capabilities()
                            if caps:
                            
                                # Declare a feature
                                feat = QgsFeature()
                            
                                # Add attributes
                                attrs = self.dlg.textAttributes.text()
                                if len(attrs) > 0:
                                    # Just use comma delimited attList
                                    attList = attrs.split(",")
                                    print attList
                                    feat.setAttributes(attList)
                                  
                                # Add the points  
                                feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(int(e), int(n))))
                                (res, outFeats) = layer.dataProvider().addFeatures([feat])
                                
                                if not res:
                                    qgis.utils.iface.messageBar().pushMessage("Error", "An error occurred adding points", level=QgsMessageBar.CRITICAL)
                                  
                                # Must update the UI for user to enjoy the new points  
                                layer.triggerRepaint()  
                                  
                            else:
                                # Active layer not writable
                                qgis.utils.iface.messageBar().pushMessage("Error", msgBadGrid, level=QgsMessageBar.CRITICAL)
                              
                    except KeyError, e:
                        qgis.utils.iface.messageBar().pushMessage("Error", msgBadGrid, level=QgsMessageBar.CRITICAL)
                        self.stayOpen = False
                        print e
                      
                    except AttributeError, e:
                        # Occurs when no layer is selected... could occur for other reasons... let me know :)
                        qgis.utils.iface.messageBar().pushMessage("Error", msgNoLayer, level=QgsMessageBar.CRITICAL)
                        self.stayOpen = False
                        print e
                
                else:
                    qgis.utils.iface.messageBar().pushMessage("Error", msgBadGrid, level=QgsMessageBar.CRITICAL)
                
            else:
                self.stayOpen = False
