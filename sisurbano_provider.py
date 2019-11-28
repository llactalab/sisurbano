# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Sisurbano
                                 A QGIS plugin
 Cáculo de indicadores urbanos
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-09-16
        copyright            : (C) 2019 by LlactaLAB
        email                : johnatan.astudillo@ucuenca.edu.ec
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

__author__ = 'Johnatan Astudillo'
__date__ = '2019-09-16'
__copyright__ = '(C) 2019 by LlactaLAB'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from .sisurbano_algorithm import SisurbanoAlgorithm

from .algs import ( 
    IA01DensityPopulation,
    IA02DensityHousing,
    IA03Compactness,
    IA04EfficiencyUseTerritory,
    IA05EmptyProperties,
    IA07proximity2BasicUrbanServices,
    IA08proximity2OpenPublicSpace,
    IA09CoverageDailyBusinessActivities,
    IA10RelationshipActivityResidence,
    IA11UrbanComplexity,
    IB01AirQuality,
    IB02LuminaryPerRoad,
    IB03AcousticComfort,
    IB05GreenPerHabitant,
    IB06Proximity2GreenPublicSpace,
    IB07SoilPermeability,
    IB08AgriculturalGrove,
    IC01PublicPedestrianRoadDistribution,
    IC03RoadsPerHabitant,
    IC04Proximity2AlternativeTransport,
    IC08ParkedVehicles,
    IC13Sewerage,
    ID03HousingRisk,
    ID10Proximity2PublicMarket,
    ID11Theft,
    ZN00CreateGrid,
    ZN01FuzzyVectorial,
    ZN02AllocateValues,
    ZN03WrapValues,
    ZN04AllocateValuesToPoints
    )


pluginPath = os.path.split(os.path.dirname(__file__))[0]

class SisurbanoProvider(QgsProcessingProvider):

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        # self.addAlgorithm(SisurbanoAlgorithm())
        self.addAlgorithm(IA01DensityPopulation.IA01DensityPopulation())
        self.addAlgorithm(IA02DensityHousing.IA02DensityHousing())
        self.addAlgorithm(IA03Compactness.IA03Compactness())
        self.addAlgorithm(IA04EfficiencyUseTerritory.IA04EfficiencyUseTerritory())
        self.addAlgorithm(IA05EmptyProperties.IA05EmptyProperties())
        self.addAlgorithm(IA07proximity2BasicUrbanServices.IA07proximity2BasicUrbanServices())
        self.addAlgorithm(IA08proximity2OpenPublicSpace.IA08proximity2OpenPublicSpace())
        self.addAlgorithm(IA09CoverageDailyBusinessActivities.IA09CoverageDailyBusinessActivities())
        self.addAlgorithm(IA10RelationshipActivityResidence.IA10RelationshipActivityResidence())
        self.addAlgorithm(IA11UrbanComplexity.IA11UrbanComplexity())
        self.addAlgorithm(IB01AirQuality.IB01AirQuality())
        self.addAlgorithm(IB02LuminaryPerRoad.IB02LuminaryPerRoad())
        self.addAlgorithm(IB03AcousticComfort.IB03AcousticComfort())
        self.addAlgorithm(IB05GreenPerHabitant.IB05GreenPerHabitant())
        self.addAlgorithm(IB06Proximity2GreenPublicSpace.IB06Proximity2GreenPublicSpace())
        self.addAlgorithm(IB07SoilPermeability.IB07SoilPermeability())
        self.addAlgorithm(IB08AgriculturalGrove.IB08AgriculturalGrove())
        self.addAlgorithm(IC01PublicPedestrianRoadDistribution.IC01PublicPedestrianRoadDistribution())
        self.addAlgorithm(IC03RoadsPerHabitant.IC03RoadsPerHabitant())
        self.addAlgorithm(IC04Proximity2AlternativeTransport.IC04Proximity2AlternativeTransport())
        self.addAlgorithm(IC08ParkedVehicles.IC08ParkedVehicles())
        self.addAlgorithm(IC13Sewerage.IC13Sewerage())
        self.addAlgorithm(ID03HousingRisk.ID03HousingRisk())
        self.addAlgorithm(ID10Proximity2PublicMarket.ID10Proximity2PublicMarket())
        self.addAlgorithm(ID11Theft.ID11Theft())
        self.addAlgorithm(ZN00CreateGrid.ZN00CreateGrid())
        self.addAlgorithm(ZN01FuzzyVectorial.ZN01FuzzyVectorial())
        self.addAlgorithm(ZN02AllocateValues.ZN02AllocateValues())
        self.addAlgorithm(ZN03WrapValues.ZN03WrapValues())
        self.addAlgorithm(ZN04AllocateValuesToPoints.ZN04AllocateValuesToPoints())


        # add additional algorithms here
        # self.addAlgorithm(MyOtherAlgorithm())

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'SISURBANO'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('SISURBANO')

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'sisurbano', 'icon_sisurbano.svg'))

    def svgIconPath(self):
        return os.path.join(pluginPath, 'sisurbano', 'icon_sisurbano.svg')        

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
