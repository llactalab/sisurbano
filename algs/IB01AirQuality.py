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
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *
from .ZHelpers import *

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class IB01AirQuality(QgsProcessingAlgorithm):
    """
    Mide la cantidad de población expuesta a niveles de emisión no
    superiores a los determiandos como nocivos para la salud. 
    Formula: (Población no expuesta a aire nocivo / Total de la población)*100
    """
    NO2 = 'NO2'
    PS = 'PS'
    SO2 = 'SO2'
    O3 = 'O3'
    BLOCKS = 'BLOCKS'
    FIELD_POPULATION = 'FIELD_POPULATION'
    FIELD_HOUSING = 'FIELD_HOUSING'
    CELL_SIZE = 'CELL_SIZE'    
    OUTPUT = 'OUTPUT'
    STUDY_AREA_GRID = 'STUDY_AREA_GRID'    




    def initAlgorithm(self, config):

        currentPath = getCurrentPath(self)
        FULL_PATH = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IB01'][1]))           
          
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
                self.O3,
                self.tr('O3 OZONO'),
                # defaultValue=None,
            )
        )          


        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.NO2,
                self.tr('NO2 DIOXIDO DE NITROGENO'),
                defaultValue=None
            )
        )
     

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.SO2,
                self.tr('SO2 DIOXIDO DE AZUFRE'),
                defaultValue=None
            )
        )   


        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.PS,
                self.tr('Ps PARTICULAS FINAS'),
                defaultValue=None
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
      maxO3 = str(100)
      maxNO2 = str(40)
      maxSO2 = str(60)
      maxPS = str(1)

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
      stByZona(params['O3'], blocks['OUTPUT'],
                                 1, [2], 'o3_', 
                                 context, feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      stByZona(params['NO2'], blocks['OUTPUT'],
                                 1, [2], 'no2_', 
                                 context, feedback)    

      steps = steps+1
      feedback.setCurrentStep(steps)
      stByZona(params['SO2'], blocks['OUTPUT'],
                                 1, [2], 'so2_', 
                                 context, feedback)                                    

      steps = steps+1
      feedback.setCurrentStep(steps)
      stByZona(params['PS'], blocks['OUTPUT'],
                                 1, [2], 'ps_', 
                                 context, feedback)  


      steps = steps+1
      feedback.setCurrentStep(steps)
      expression = 'id_blocks != -100'


      comodin = filterByExpression(blocks['OUTPUT'], expression, context, feedback)
                   

 
      condition = "CASE WHEN (o3_mean > "+maxO3 + \
                  " OR no2_mean > "+maxNO2 + \
                  " OR so2_mean > "+maxSO2 + \
                  " OR ps_mean > "+maxPS + \
                  ") THEN 1" + \
                  " ELSE 0" + \
                  " END"         


      # print(condition)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksPull = calculateField(comodin['OUTPUT'], 'is_pull',
                                        condition,
                                        context,
                                        feedback, type=1)     

                                                                                              

      steps = steps+1
      feedback.setCurrentStep(steps)
      segments = intersection(blocksPull['OUTPUT'], gridNeto['OUTPUT'],
                              ['is_pull', fieldHousing],
                              'id_grid',
                              context, feedback)

      # Haciendo el buffer inverso aseguramos que los segmentos
      # quden dentro de la malla
      steps = steps+1
      feedback.setCurrentStep(steps)
      pullForSegmentsFixed = makeSureInside(segments['OUTPUT'],
                                                  context,
                                                  feedback)
      # Con esto se saca el total de viviendas
      steps = steps+1
      feedback.setCurrentStep(steps)
      gridNetoAndSegmentsPull = joinByLocation(gridNeto['OUTPUT'],
                                           pullForSegmentsFixed['OUTPUT'],
                                           [fieldHousing],
                                           [CONTIENE], [SUM], UNDISCARD_NONMATCHING,                 
                                           context,
                                           feedback)

      #descartar NULL para obtener el total de viviendas que cumple
      steps = steps+1
      feedback.setCurrentStep(steps)
      pullActiveForSegmentsFixed = filter(pullForSegmentsFixed['OUTPUT'],
                                                 'is_pull', IGUAL,
                                                 '0', context, feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      gridNetoAndSegmentsNotNull = joinByLocation(gridNetoAndSegmentsPull['OUTPUT'],
                                                  pullActiveForSegmentsFixed['OUTPUT'],
                                                  [fieldHousing, 'is_pull'],
                                                  [CONTIENE], [SUM], UNDISCARD_NONMATCHING,               
                                                  context,
                                                  feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      formulaPull = 'coalesce((coalesce('+fieldHousing+'_sum_2,0) /  coalesce('+fieldHousing+'_sum,0))*100, "")'
      pull = calculateField(gridNetoAndSegmentsNotNull['OUTPUT'], NAMES_INDEX['IB01'][0],
                                        formulaPull,
                                        context,
                                        feedback,  params['OUTPUT'])


      return pull


    def icon(self):
        return QIcon(os.path.join(pluginPath, 'sisurbano', 'icons', 'air.png'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'B01 Calidad del aire'

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
        return IB01AirQuality()

