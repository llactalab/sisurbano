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
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *
from .ZHelpers import *

#pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class IA08proximity2OpenPublicSpace(QgsProcessingAlgorithm):
    """
    Mide la población que se encuentra próxima a espacios públicos abiertos.
    Porcentaje de viviendas ubicadas a una caminata de 5 minutos o menos de
    un espacio público abierto (parques, plazas, parques cívicos, parque infantil,
    campo deportivo, margen de agua, parque lineal, bulevards y mercados abiertos). 
    Formula: (Viviendas con cobertura simultánea de actividades comerciales cotidianas / Viviendas totales)*100
    """ 
    BLOCKS = 'BLOCKS'
    # FIELD_POPULATION = 'FIELD_POPULATION'
    FIELD_HOUSING = 'FIELD_HOUSING'
    EQUIPMENT_PUBLIC_SPACE = 'EQUIPMENT_PUBLIC_SPACE'
    CELL_SIZE = 'CELL_SIZE'    
    OUTPUT = 'OUTPUT'
    DISTANCE_BUFFER = 300
    STUDY_AREA_GRID = 'STUDY_AREA_GRID'  

    DISTANCE_OPTIONS = 'DISTANCE_OPTIONS'
    ROADS = 'ROADS'


    def initAlgorithm(self, config):
        currentPath = getCurrentPath(self)
        FULL_PATH = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IA08'][1]))           


        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BLOCKS,
                self.tr('Manzanas'),
                [QgsProcessing.TypeVectorPolygon]
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
          QgsProcessingParameterEnum(
          self.DISTANCE_OPTIONS,
          self.tr('Tipo de distancia'),
          options=['ISOCRONA','RADIAL'], 
          allowMultiple=False, 
          defaultValue=1)
        )            


        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ROADS,
                self.tr('Red vial (obligatorio para distancia ISOCRONA)'),
                [QgsProcessing.TypeVectorLine],
                optional = True,
                defaultValue = ''
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
                self.EQUIPMENT_PUBLIC_SPACE,
                self.tr('Espacios públicos abiertos'),
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
      totalStpes = 13
      # fieldPopulation = params['FIELD_POPULATION']
      fieldHousing = params['FIELD_HOUSING']

      feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)

      """
      -----------------------------------------------------------------
      Calcular las facilidades a espacios pubicos abiertos
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
      blocks = calculateArea(params['BLOCKS'], 'area_bloc', context,
                             feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      segments = intersection(blocks['OUTPUT'], gridNeto['OUTPUT'],
                              'osp_idx_count;area_bloc;' + fieldHousing,
                              'id_grid',
                              context, feedback, )

      steps = steps+1
      feedback.setCurrentStep(steps)
      segmentsArea = calculateArea(segments['OUTPUT'],
                                   'area_seg',
                                   context, feedback)


      steps = steps+1
      feedback.setCurrentStep(steps)
      formulaHousingSegments = '(area_seg/area_bloc) * ' + fieldHousing
      housingForSegments = calculateField(segmentsArea['OUTPUT'], 'h_s',
                                          formulaHousingSegments,
                                          context,
                                          feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksWithId = calculateField(housingForSegments['OUTPUT'], 'id_block', '$id', context,
                                    feedback, type=1)

      steps = steps+1
      feedback.setCurrentStep(steps)
      equipmentWithId = calculateField(params['EQUIPMENT_PUBLIC_SPACE'], 'idx', '$id', context,
                                      feedback, type=1)      

      steps = steps+1
      feedback.setCurrentStep(steps)
      centroidsBlocks = createCentroids(blocksWithId['OUTPUT'], context,
                                        feedback)      

      result = []

      print(params['DISTANCE_OPTIONS'] )

      if(params['DISTANCE_OPTIONS'] == 0):
        steps = steps+1
        feedback.setCurrentStep(steps)        
        feedback.pushConsoleInfo(str(('Cálculo de áreas de servicio'))) 
        serviceArea = bufferIsocrono(params['ROADS'], equipmentWithId['OUTPUT'], TIME_TRAVEL_COST, STRATEGY_TIME, context, feedback)


        steps = steps+1
        feedback.setCurrentStep(steps)
        housingServed = intersection(segmentsArea['OUTPUT'], serviceArea['OUTPUT'],
                                [fieldHousing,'area_bloc'],
                                ['id_grid'],
                                context, feedback)


        steps = steps+1
        feedback.setCurrentStep(steps)
        areaHousingServed = calculateArea(housingServed['OUTPUT'],
                                     'area_served',
                                     context, feedback)                


        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaHousingSegmentsServed = '(area_served/area_bloc) * ' + fieldHousing
        housingSegmentsServed = calculateField(areaHousingServed['OUTPUT'], 'has',
                                            formulaHousingSegmentsServed,
                                            context,
                                            feedback)    

        steps = steps+1
        feedback.setCurrentStep(steps)
        housingSegmentsServedFixed = makeSureInside(housingSegmentsServed['OUTPUT'],
                                                    context,
                                                    feedback)    
        steps = steps+1
        feedback.setCurrentStep(steps)
        gridNetoAndSegmentsServed = joinByLocation(gridNeto['OUTPUT'],
                                             housingSegmentsServedFixed['OUTPUT'],
                                             'has',
                                             [CONTIENE], [SUM], UNDISCARD_NONMATCHING,                 
                                             context,
                                             feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        housingForSegmentsFixed = makeSureInside(housingForSegments['OUTPUT'],
                                                    context,
                                                    feedback)    

        steps = steps+1
        feedback.setCurrentStep(steps)
        gridNetoAndSegmentsServed = joinByLocation(gridNetoAndSegmentsServed['OUTPUT'],
                                             housingForSegmentsFixed['OUTPUT'],
                                             'h_s',
                                             [CONTIENE], [SUM], UNDISCARD_NONMATCHING,                 
                                             context,
                                             feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaProximity = 'coalesce((coalesce(has_sum,0) /  coalesce(h_s_sum,""))*100, "")'
        proximity2OpenSpace = calculateField(gridNetoAndSegmentsServed['OUTPUT'], NAMES_INDEX['IA08'][0],
                                          formulaProximity,
                                          context,
                                          feedback,  params['OUTPUT'])        


        result = proximity2OpenSpace
    
      else:
        feedback.pushConsoleInfo(str(('Cálculo de buffer radial')))   
        steps = steps+1
        feedback.setCurrentStep(steps)
        blockBuffer4OpenSapace = createBuffer(centroidsBlocks['OUTPUT'], self.DISTANCE_BUFFER,
                                              context,
                                              feedback,)

        steps = steps+1
        feedback.setCurrentStep(steps)
        counterOpenSpace = joinByLocation(blockBuffer4OpenSapace['OUTPUT'],
                                          equipmentWithId['OUTPUT'],
                                          'idx', [CONTIENE, INTERSECTA], [COUNT],
                                          UNDISCARD_NONMATCHING,
                                          context,
                                          feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        blocksJoined = joinByAttr(blocksWithId['OUTPUT'], 'id_block',
                                  counterOpenSpace['OUTPUT'], 'id_block',
                                  'idx_count',
                                  UNDISCARD_NONMATCHING,
                                  'osp_',
                                  context,
                                  feedback)

        """
        -----------------------------------------------------------------
        Calcular numero de viviendas por hexagano
        -----------------------------------------------------------------
        """


        # Haciendo el buffer inverso aseguramos que los segmentos
        # quden dentro de la malla
        steps = steps+1
        feedback.setCurrentStep(steps)
        facilitiesForSegmentsFixed = makeSureInside(blocksJoined['OUTPUT'],
                                                    context,
                                                    feedback)
        # Con esto se saca el total de viviendas
        steps = steps+1
        feedback.setCurrentStep(steps)
        gridNetoAndSegments = joinByLocation(gridNeto['OUTPUT'],
                                             facilitiesForSegmentsFixed['OUTPUT'],
                                             'osp_idx_count;h_s',
                                             [CONTIENE], [SUM], UNDISCARD_NONMATCHING,                 
                                             context,
                                             feedback)

        #descartar NULL para obtener el total de viviendas que cumple
        steps = steps+1
        feedback.setCurrentStep(steps)
        facilitiesNotNullForSegmentsFixed = filter(facilitiesForSegmentsFixed['OUTPUT'],
                                                   'osp_idx_count', NOT_NULL,
                                                   '', context, feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        gridNetoAndSegmentsNotNull = joinByLocation(gridNetoAndSegments['OUTPUT'],
                                                    facilitiesNotNullForSegmentsFixed['OUTPUT'],
                                                    'h_s',
                                                    [CONTIENE], [SUM], UNDISCARD_NONMATCHING,               
                                                    context,
                                                    feedback)

        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaProximity = 'coalesce((coalesce(h_s_sum_2,0) /  coalesce(h_s_sum,""))*100, "")'
        proximity2OpenSpace = calculateField(gridNetoAndSegmentsNotNull['OUTPUT'], NAMES_INDEX['IA08'][0],
                                          formulaProximity,
                                          context,
                                          feedback,  params['OUTPUT'])

        result = proximity2OpenSpace

      return result


        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        #return {self.OUTPUT: dest_id}

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'openspace.jpeg'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'A08 Proximidad al espacio público abierto'

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
        return IA08proximity2OpenPublicSpace()

    def shortHelpString(self):
        return  "<b>Descripción:</b><br/>"\
                "<span>Mide la población que se encuentra próxima a espacios públicos abiertos. Porcentaje de viviendas ubicadas a una caminata de 5 minutos o menos de un espacio público abierto (parques, plazas, parques cívicos, parque infantil, campo deportivo, margen de agua, parque lineal, bulevards y mercados abiertos).</span>"\
                "<br/><br/><b>Justificación y metodología:</b><br/>"\
                "<span>Áreas cubiertas se consideran aquellas que simultáneamente quedan cubiertas al trazar un radio de 300m desde cada tipo de actividad comercial cotidiana. Actividades comerciales cotidianas se consideran las siguientes categorías: a) tienda de abarrotes, despensas, minimercado, b) farmacia, droguería, c) papelería, bazar, d) panadería, heladería, pastelería, e) depósitos de distribución de cilindros de gas. Usar distancia isocrona</span>"\
                "<br/><br/><b>Formula:</b><br/>"\
                "<span>(Viviendas con cobertura simultánea de actividades comerciales cotidianas / Viviendas totales)*100<br/>"        

