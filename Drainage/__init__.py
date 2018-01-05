# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Drainage
                                 A QGIS plugin
 Drainage
                             -------------------
        begin                : 2017-04-14
        copyright            : (C) 2017 by HermeSys
        email                : shpark@hermesys.co.kr
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
    """Load Drainage class from file Drainage.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Drainage import Drainage
    return Drainage(iface)
