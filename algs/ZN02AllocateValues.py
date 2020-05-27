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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing,
                       QgsProcessingMultiStepFeedback,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *

#pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class ZN02AllocateValues(QgsProcessingAlgorithm):
    """
    Distribuye la población de las manzanas a los puntos o medidores
    más cercanos al polígono de la manzana
    """  
    BLOCKS = 'BLOCKS'
    POINTS = 'POINTS'
    FIELD_POPULATION = 'FIELD_POPULATION'
    FIELD_HOUSING = 'FIELD_HOUSING'
    OUTPUT = 'OUTPUT'
    STUDY_AREA_GRID = 'STUDY_AREA_GRID'

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BLOCKS,
                self.tr('Manzanas'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD_POPULATION,
                self.tr('Población'),
                'poblacion', 'BLOCKS'
            )
        )        

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD_HOUSING,
                self.tr('Viviendas'),
                'viviendas', 'BLOCKS'
            )
        )           

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POINTS,
                self.tr('Medidores'),
                [QgsProcessing.TypeVectorPoint]
            )
        )


        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.STUDY_AREA_GRID,
                self.tr(TEXT_GRID_INPUT),
                [QgsProcessing.TypeVectorPolygon],
                '', OPTIONAL_GRID_INPUT
            )
        )        

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Salida')
            )
        )

    def processAlgorithm(self, params, context, feedback):
        steps = 0
        totalStpes = 6
        fieldPopulation = params['FIELD_POPULATION']
        fieldHousing = params['FIELD_HOUSING']
        DISCARD = True
        UNDISCARD = False

        feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)    

        steps = steps+1
        feedback.setCurrentStep(steps)
        blocksWithId = calculateField(params['BLOCKS'], 'id_block', '$id', context,
                                      feedback, type=1)   


        steps = steps+1
        feedback.setCurrentStep(steps)
        pointsJoined = joinAttrByNear(params['POINTS'],
                                      blocksWithId['OUTPUT'], [],
                                      UNDISCARD,
                                      'blk_',
                                      5,
                                      1,
                                      context,
                                      feedback)


        steps = steps+1
        feedback.setCurrentStep(steps)
        statistics = statisticsByCategories(pointsJoined['OUTPUT'], 
                                            ['blk_id_block'],
                                            None,
                                            context,
                                            feedback)


        steps = steps+1
        feedback.setCurrentStep(steps)
        pointsJoinedStast = joinByAttr(pointsJoined['OUTPUT'], 
                                       'blk_id_block',
                                       statistics['OUTPUT'], 
                                       'blk_id_block',
                                       'count',
                                       DISCARD,
                                       'st_',
                                       context,
                                       feedback)   


        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaPopulationPerPoint = 'blk_' + fieldPopulation + ' / st_count' 
        populationPerPoint = calculateField(pointsJoinedStast['OUTPUT'],
                                       'population',
                                       formulaPopulationPerPoint,
                                       context,
                                       feedback)    


        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaHousingPerPoint = 'blk_' + fieldHousing + ' / st_count' 
        housingPerPoint = calculateField(populationPerPoint['OUTPUT'],
                                       'housing',
                                       formulaHousingPerPoint,
                                       context,
                                       feedback)    


        gridPopulation= joinByLocation(params['STUDY_AREA_GRID'],
                                             housingPerPoint['OUTPUT'],
                                             'population;housing',                                   
                                              [CONTIENE], [SUM],
                                              UNDISCARD_NONMATCHING,
                                              context,
                                              feedback,  params['OUTPUT'])   

        return gridPopulation    

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        #return {self.OUTPUT: dest_id}
                                          
    def icon(self):
        return QIcon(os.path.join(pluginPath, 'hexpo.jpg'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Z02 Distribuir valores polígono a malla'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Z General'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ZN02AllocateValues()

    def shortHelpString(self):
        return  "<b>Descripción:</b><br/>"\
                "<span>Distribuye proporcionalemente el valor del polígono a los puntos que intersecten o esten cerca con este y se agrega a la malla.</span>"