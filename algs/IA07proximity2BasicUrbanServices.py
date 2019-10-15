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
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *
from .ZHelpers import *

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class IA07proximity2BasicUrbanServices(QgsProcessingAlgorithm):
    """
    Mide la población que se encuentra próxima de manera simultanea a los
    diferentes tipos de equipamiento urbano (educación, salud, cultural y
    recreación). Relación entre el número de viviendas a 500m de equipamientos
    educativos, a 1200m de equipamientos de salud, a 400m de equipamientos
    culturales y a 1000m de equipamientos deportivos-recreativos,
    con respecto al total de viviendas en el área de estudio.
    Formula: (Viviendas con proximidad simultánea a todos los tipos
    de equipamiento / Viviendas totales) * 100
    """ 
    BLOCKS = 'BLOCKS'
    EDUCATION = 'EDUCATION'
    HEALTH = 'HEALTH'
    CULTURE = 'CULTURE'
    SPORTS = 'SPORTS'    
    FIELD_POPULATION = 'FIELD_POPULATION'
    FIELD_HOUSING = 'FIELD_HOUSING'
    CELL_SIZE = 'CELL_SIZE'    
    OUTPUT = 'OUTPUT'
    STUDY_AREA_GRID = 'STUDY_AREA_GRID'

 

    def initAlgorithm(self, config):
        currentPath = getCurrentPath(self)    
        FULL_PATH = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IA07'][1]))    
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
                self.STUDY_AREA_GRID,
                self.tr(TEXT_GRID_INPUT),
                [QgsProcessing.TypeVectorPolygon],
                '', OPTIONAL_GRID_INPUT
            )
        )

        if OPTIONAL_GRID_INPUT:
            self.addParameter(
                QgsProcessingParameterNumber(
                    self.CELL_SIZE,
                    self.tr('Tamaño de la malla'),
                    QgsProcessingParameterNumber.Integer,
                    P_CELL_SIZE, False, 1, 99999999
                )
            )       

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.EDUCATION,
                self.tr('Educación'),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.HEALTH,
                self.tr('Salud'),
                [QgsProcessing.TypeVectorPoint]
            )
        )  

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.CULTURE,
                self.tr('Cultura'),
                [QgsProcessing.TypeVectorPoint]
            )
        )    

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.SPORTS,
                self.tr('Bienestar social'),
                [QgsProcessing.TypeVectorPoint]
            )
        )                           

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Salida'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH)                
            )
        )

    def processAlgorithm(self, params, context, feedback):
        steps = 0
        totalStpes = 28
        fieldPopulation = params['FIELD_POPULATION']
        fieldHousing = params['FIELD_HOUSING']
        DISTANCE_EDUCATION = 500
        DISTANCE_HEALTH = 1200
        DISTANCE_CULTURE = 400
        DISTANCE_SPORTS = 1000


        feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)

        """
        -----------------------------------------------------------------
        Calcular las facilidades
        -----------------------------------------------------------------
        """

        steps = steps+1
        feedback.setCurrentStep(steps)
        blocksWithId = calculateField(params['BLOCKS'], 'id_block', '$id', context,
                                      feedback, type=1)

        steps = steps+1
        feedback.setCurrentStep(steps)
        centroidsBlocks = createCentroids(blocksWithId['OUTPUT'], context,
                                          feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        blockBuffer4Education = createBuffer(centroidsBlocks['OUTPUT'], DISTANCE_EDUCATION,
                                             context,
                                             feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        blockBuffer4Health = createBuffer(centroidsBlocks['OUTPUT'], DISTANCE_HEALTH, context,
                                          feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        blockBuffer4Culture = createBuffer(centroidsBlocks['OUTPUT'], DISTANCE_CULTURE, context,
                                           feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        BlockBuffer4Sports = createBuffer(centroidsBlocks['OUTPUT'], DISTANCE_SPORTS,
                                          context, feedback)


        steps = steps+1
        feedback.setCurrentStep(steps)
        layerEducation = calculateField(params['EDUCATION'], 'idx', '$id', context,
                                       feedback, type=1)


        steps = steps+1
        feedback.setCurrentStep(steps)
        layerHealth = calculateField(params['HEALTH'], 'idx', '$id', context,
                                      feedback, type=1)      


        steps = steps+1
        feedback.setCurrentStep(steps)
        layerCulture = calculateField(params['CULTURE'], 'idx', '$id', context,
                                      feedback, type=1)                                             


        steps = steps+1
        feedback.setCurrentStep(steps)
        layerSports = calculateField(params['SPORTS'], 'idx', '$id', context,
                                     feedback, type=1) 


        layerEducation = layerEducation['OUTPUT']
        layerHealth = layerHealth['OUTPUT']
        layerCulture = layerCulture['OUTPUT']
        layerSports = layerSports['OUTPUT']


        steps = steps+1
        feedback.setCurrentStep(steps)
        counterEducation = joinByLocation(blockBuffer4Education['OUTPUT'],
                                          layerEducation,
                                          'idx', [CONTIENE], [COUNT],
                                          UNDISCARD_NONMATCHING,
                                          context,
                                          feedback)
        steps = steps+1
        feedback.setCurrentStep(steps)
        counterHealth = joinByLocation(blockBuffer4Health['OUTPUT'],
                                       layerHealth,
                                       'idx', [CONTIENE], [COUNT],
                                       UNDISCARD_NONMATCHING,
                                       context,
                                       feedback)
        steps = steps+1
        feedback.setCurrentStep(steps)
        counterCulture = joinByLocation(blockBuffer4Culture['OUTPUT'],
                                        layerCulture,
                                        'idx', [CONTIENE], [COUNT],
                                        UNDISCARD_NONMATCHING,
                                        context,
                                        feedback)
        steps = steps+1
        feedback.setCurrentStep(steps)
        counterSport = joinByLocation(BlockBuffer4Sports['OUTPUT'],
                                      layerSports,
                                      'idx', [CONTIENE], [COUNT],
                                      UNDISCARD_NONMATCHING,
                                      context,
                                      feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        blocksJoined = joinByAttr(blocksWithId['OUTPUT'], 'id_block',
                                  counterEducation['OUTPUT'], 'id_block',
                                  'idx_count',
                                  UNDISCARD_NONMATCHING,
                                  'edu_',
                                  context,
                                  feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        blocksJoined = joinByAttr(blocksJoined['OUTPUT'], 'id_block',
                                  counterHealth['OUTPUT'], 'id_block',
                                  'idx_count',
                                  UNDISCARD_NONMATCHING,
                                  'hea_',
                                  context,
                                  feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        blocksJoined = joinByAttr(blocksJoined['OUTPUT'], 'id_block',
                                  counterCulture['OUTPUT'], 'id_block',
                                  'idx_count',
                                  UNDISCARD_NONMATCHING,
                                  'cul_',
                                  context,
                                  feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        blocksJoined = joinByAttr(blocksJoined['OUTPUT'], 'id_block',
                                  counterSport['OUTPUT'], 'id_block',
                                  'idx_count',
                                  UNDISCARD_NONMATCHING,
                                  'spo_',
                                  context,
                                  feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaFacilities = 'edu_idx_count * hea_idx_count * cul_idx_count * spo_idx_count'
        blocksFacilities = calculateField(blocksJoined['OUTPUT'], 'facilities',
                                          formulaFacilities,
                                          context,
                                          feedback)

        """
        -----------------------------------------------------------------
        Calcular numero de viviendas por hexagano
        -----------------------------------------------------------------
        """
        steps = steps+1
        feedback.setCurrentStep(steps)
        if not OPTIONAL_GRID_INPUT: params['CELL_SIZE'] = P_CELL_SIZE        
        grid, isStudyArea = buildStudyArea(params['CELL_SIZE'], params['BLOCKS'],
                                           params['STUDY_AREA_GRID'],
                                           context, feedback)
        gridNeto = grid

        steps = steps+1
        feedback.setCurrentStep(steps)
        segments = intersection(blocksFacilities['OUTPUT'], gridNeto['OUTPUT'],
                                'edu_idx_count;hea_idx_count;cul_idx_count;spo_idx_count;facilities;' + fieldHousing,
                                'id_grid',
                                context, feedback)

        # Haciendo el buffer inverso aseguramos que los segmentos
        # quden dentro de la malla
        steps = steps+1
        feedback.setCurrentStep(steps)
        facilitiesForSegmentsFixed = makeSureInside(segments['OUTPUT'],
                                                    context,
                                                    feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        gridNetoAndSegments = joinByLocation(gridNeto['OUTPUT'],
                                             facilitiesForSegmentsFixed['OUTPUT'],
                                             'edu_idx_count;hea_idx_count;cul_idx_count;spo_idx_count;facilities;' + fieldHousing,
                                             [CONTIENE],
                                             [MAX, SUM], UNDISCARD_NONMATCHING,                 
                                             context,
                                             feedback)
        # tomar solo los que tienen cercania simultanea (descartar NULL)
        steps = steps+1
        feedback.setCurrentStep(steps)
        facilitiesNotNullForSegmentsFixed = filter(facilitiesForSegmentsFixed['OUTPUT'],
                                                   'facilities', NOT_NULL,
                                                   '', context, feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        gridNetoAndSegmentsNotNull = joinByLocation(gridNeto['OUTPUT'],
                                                    facilitiesNotNullForSegmentsFixed['OUTPUT'],
                                                    fieldHousing,
                                                    [CONTIENE],
                                                    [MAX, SUM], UNDISCARD_NONMATCHING,               
                                                    context,
                                                    feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        totalHousing = joinByAttr(gridNetoAndSegments['OUTPUT'], 'id_grid',
                                  gridNetoAndSegmentsNotNull['OUTPUT'], 'id_grid',
                                  fieldHousing+'_sum',
                                  UNDISCARD_NONMATCHING,
                                  'net_',
                                  context,
                                  feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaProximity = '(coalesce(net_'+fieldHousing+'_sum,0) /  coalesce('+fieldHousing+'_sum,0))*100'
        proximity2BasicU = calculateField(totalHousing['OUTPUT'], NAMES_INDEX['IA07'][0],
                                          formulaProximity,
                                          context,
                                          feedback,  params['OUTPUT'])

        return proximity2BasicU

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        #return {self.OUTPUT: dest_id}

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'sisurbano', 'icons', 'icon_servicearea_contour_multiple.svg'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'A07 Proximidad a servicios urbanos básicos'

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
        return 'A Ambiente construido'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return IA07proximity2BasicUrbanServices()

