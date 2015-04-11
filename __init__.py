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
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load BritNatGridRef class from file BritNatGridRef.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .BritNatGridRef import BritNatGridRef
    return BritNatGridRef(iface)
