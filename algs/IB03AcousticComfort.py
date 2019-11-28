# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Sisurbano
                                 A QGIS plugin
 Cáculo de indicadores urbanos
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-11-21
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
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *
from .ZHelpers import *

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class IB03AcousticComfort(QgsProcessingAlgorithm):
    """
    Mide la cantidad de población expuesta a niveles sonoros superiores a
    los recomendados que comprenden 65 dB diurnos y 55 dB nocturnos. 
    Formula: (Población expuesta a niveles acústicos
    inferiores a los límites establecidos / Población total)*100
    """
    NOISE_NIGHT = 'NOISE_NIGHT'
    NOISE_DAY = 'NOISE_DAY'
    BLOCKS = 'BLOCKS'
    FIELD_POPULATION = 'FIELD_POPULATION'
    FIELD_HOUSING = 'FIELD_HOUSING'
    CELL_SIZE = 'CELL_SIZE'    
    OUTPUT = 'OUTPUT'
    STUDY_AREA_GRID = 'STUDY_AREA_GRID'    

    def initAlgorithm(self, config):

        currentPath = getCurrentPath(self)
        FULL_PATH = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IB03'][1]))           
          
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
            QgsProcessingParameterRasterLayer(
                self.NOISE_DAY,
                self.tr('Ruido día'),
                defaultValue=None
            )
        )
     

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.NOISE_NIGHT,
                self.tr('Ruido noche'),
                # defaultValue=None,
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
      totalStpes = 14
      fieldPopulation = params['FIELD_POPULATION']
      fieldHousing = params['FIELD_HOUSING']
      maxDay = str(70)
      maxNight = str(65)

      feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)


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
      blocks = calculateField(params['BLOCKS'], 'id_blocks', '$id', context,
                                    feedback, type=1)          

      steps = steps+1
      feedback.setCurrentStep(steps)
      stByZona(params['NOISE_DAY'], blocks['OUTPUT'],
                                 1, [2], 'nd_', 
                                 context, feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      stByZona(params['NOISE_NIGHT'], blocks['OUTPUT'],
                                 1, [2], 'nn_', 
                                 context, feedback)    


      steps = steps+1
      feedback.setCurrentStep(steps)
      expression = 'id_blocks != -100'


      comodin = filterByExpression(blocks['OUTPUT'], expression, context, feedback)
                   

 
      condition = "CASE WHEN (nd_mean > "+maxDay + \
                  " OR nn_mean > "+maxNight + \
                  ") THEN 1" + \
                  " ELSE 0" + \
                  " END"         


      # print(condition)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksNoise = calculateField(comodin['OUTPUT'], 'is_noise',
                                        condition,
                                        context,
                                        feedback, type=1)     

                                                                                              

      steps = steps+1
      feedback.setCurrentStep(steps)
      segments = intersection(blocksNoise['OUTPUT'], gridNeto['OUTPUT'],
                              ['is_noise', fieldHousing],
                              'id_grid',
                              context, feedback)

      # Haciendo el buffer inverso aseguramos que los segmentos
      # quden dentro de la malla
      steps = steps+1
      feedback.setCurrentStep(steps)
      noiseForSegmentsFixed = makeSureInside(segments['OUTPUT'],
                                                  context,
                                                  feedback)
      # Con esto se saca el total de viviendas
      steps = steps+1
      feedback.setCurrentStep(steps)
      gridNetoAndSegmentsNoise = joinByLocation(gridNeto['OUTPUT'],
                                           noiseForSegmentsFixed['OUTPUT'],
                                           [fieldHousing],
                                           [CONTIENE], [SUM], UNDISCARD_NONMATCHING,                 
                                           context,
                                           feedback)

      #descartar NULL para obtener el total de viviendas que cumple
      steps = steps+1
      feedback.setCurrentStep(steps)
      pullActiveForSegmentsFixed = filter(noiseForSegmentsFixed['OUTPUT'],
                                                 'is_noise', IGUAL,
                                                 '0', context, feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      gridNetoAndSegmentsNotNull = joinByLocation(gridNetoAndSegmentsNoise['OUTPUT'],
                                                  pullActiveForSegmentsFixed['OUTPUT'],
                                                  [fieldHousing, 'is_noise'],
                                                  [CONTIENE], [SUM], UNDISCARD_NONMATCHING,               
                                                  context,
                                                  feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      formulaNoise = 'coalesce((coalesce('+fieldHousing+'_sum_2,0) /  coalesce('+fieldHousing+'_sum,0))*100, "")'
      noise = calculateField(gridNetoAndSegmentsNotNull['OUTPUT'], NAMES_INDEX['IB03'][0],
                                        formulaNoise,
                                        context,
                                        feedback,  params['OUTPUT'])


      return noise


    def icon(self):
        return QIcon(os.path.join(pluginPath, 'sisurbano', 'icons', 'noise3.png'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'B03 Confort acústico'

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
        return 'B Ambiente biofísico'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return IB03AcousticComfort()

