# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Sisurbano
                                 A QGIS plugin
 Cáculo de indicadores urbanos
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-12-09
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
__date__ = '2019-10-12'
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

class IC00WrapC(QgsProcessingAlgorithm):
    """
    Calcula todos los indicadores de ambiente construido
    """
    BLOCKS = 'BLOCKS'
    FIELD_POPULATION = 'FIELD_POPULATION'
    FIELD_HOUSING = 'FIELD_HOUSING'    
    CELL_SIZE = 'CELL_SIZE'
    STUDY_AREA_GRID = 'STUDY_AREA_GRID'

    #-----------------C01----------------------
    WALK_ROAD = 'WALK_ROAD'
    ROADS = 'ROADS'
    #-----------------C03----------------------
    ROADS_LINES = 'ROADS_LINES'
    #-----------------C04----------------------
    BUSSTOP = 'BUSSTOP'    
    TRAMSTOP = 'TRAMSTOP'    
    BIKESTOP = 'BIKESTOP'    
    BIKEWAY = 'BIKEWAY'    
    CROSSWALK = 'CROSSWALK'
    #-----------------C08----------------------
    PARKING = 'PARKING'
    AREA_PER_PARKING = 'AREA_PER_PARKING'
    #-----------------C13----------------------
    SEWERAGE = 'SEWERAGE'
    #-----------------OUTPUTS----------------------
    OUTPUT_C01 = 'OUTPUT_C01'
    OUTPUT_C03 = 'OUTPUT_C03'
    OUTPUT_C04 = 'OUTPUT_C04'
    OUTPUT_C08 = 'OUTPUT_C08'
    OUTPUT_C13 = 'OUTPUT_C13'


    def initAlgorithm(self, config):

        currentPath = getCurrentPath(self)
        FULL_PATH_C01 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC01'][1]))
        FULL_PATH_C03 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC03'][1]))
        FULL_PATH_C04 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC04'][1]))
        FULL_PATH_C08 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC08'][1]))
        FULL_PATH_C13 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC13'][1]))

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

    #-----------------C01----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ROADS,
                self.tr('Viario público'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.WALK_ROAD,
                self.tr('Viario público peatonal'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )    
    #-----------------C03----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ROADS_LINES,
                self.tr('Vías públicas'),
                [QgsProcessing.TypeVectorLine]
            )
        )
    #-----------------C04----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BUSSTOP,
                self.tr('Paradas de bus'),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.TRAMSTOP,
                self.tr('Tranvía'),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BIKESTOP,
                self.tr('Bici pública'),
                [QgsProcessing.TypeVectorPoint]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BIKEWAY,
                self.tr('Ciclovía'),
                [QgsProcessing.TypeVectorLine]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.CROSSWALK,
                self.tr('Caminos peatonales'),
                [QgsProcessing.TypeVectorLine]
            )
        )                                
    #-----------------C08----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.PARKING,
                self.tr('Puestos de parqueo'),
                [QgsProcessing.TypeVectorPoint]
            )
        ) 

        self.addParameter(
            QgsProcessingParameterNumber(
                self.AREA_PER_PARKING,
                self.tr('Área de cada parqueadero'),
                QgsProcessingParameterNumber.Integer,
                10, False, 1, 99999999
            )
        )  
    #-----------------C13----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.SEWERAGE,
                self.tr('Cobertura alcantarillado)'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )


    #-----------------OTHERS----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.STUDY_AREA_GRID,
                self.tr(TEXT_GRID_INPUT),
                [QgsProcessing.TypeVectorPolygon],
                '', OPTIONAL_GRID_INPUT
            )
        )

    #-----------------OUTPUTS----------------------

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_C01,
                self.tr('C01 Reparto del viario público peatonal'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_C01)
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_C03,
                self.tr('C03 Vías públicas por habitante'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_C03)
            )
        )    

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_C04,
                self.tr('C04 Proximidad a redes de transporte alternativo'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_C04)
            )
        )                  

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_C08,
                self.tr('C08 Espacio público ocupado por vehículos parqueados'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_C08)
            )
        )  

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_C13,
                self.tr('C13 Cobertura del servicio de alcantarillado'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_C13)
            )
        )  

           

    def processAlgorithm(self, params, context, feedback):
        steps = 0
        totalStpes = 6
        outputs = {}
        results = {}
        feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)

        # C01 Reparto del viario público peatonal
        steps = steps+1
        feedback.setCurrentStep(steps)  
        if feedback.isCanceled():
            return {}
        alg_params = {
            'ROADS': params['ROADS'],
            'STUDY_AREA_GRID': params['STUDY_AREA_GRID'],
            'WALK_ROAD': params['WALK_ROAD'],
            'OUTPUT': params['OUTPUT_C01']
        }
        outputs['C01RepartoDelViarioPblicoPeatonal'] = processing.run('SISURBANO:C01 Reparto del viario público peatonal', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['OUTPUT_C01'] = outputs['C01RepartoDelViarioPblicoPeatonal']['OUTPUT'] 

       # C03 Vías públicas por habitante
        steps = steps+1
        feedback.setCurrentStep(steps)  
        if feedback.isCanceled():
            return {}       
        alg_params = {
            'BLOCKS': params['BLOCKS'],
            'FIELD_POPULATION': params['FIELD_POPULATION'],
            'ROADS_LINES': params['ROADS_LINES'],
            'STUDY_AREA_GRID': params['STUDY_AREA_GRID'],
            'OUTPUT': params['OUTPUT_C03']
        }
        outputs['C03VasPblicasPorHabitante'] = processing.run('SISURBANO:C03 Vías públicas por habitante', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['OUTPUT_C03'] = outputs['C03VasPblicasPorHabitante']['OUTPUT']   

        # C04 Proximidad a redes de transporte alternativo
        steps = steps+1
        feedback.setCurrentStep(steps)  
        if feedback.isCanceled():
            return {}           
        alg_params = {
            'BIKESTOP': params['BIKESTOP'],
            'BIKEWAY': params['BIKEWAY'],
            'BLOCKS': params['BLOCKS'],
            'BUSSTOP': params['BUSSTOP'],
            'CROSSWALK': params['CROSSWALK'],
            'FIELD_POPULATE_HOUSING': params['FIELD_POPULATION'],
            'STUDY_AREA_GRID': params['STUDY_AREA_GRID'],
            'TRAMSTOP': params['TRAMSTOP'],
            'OUTPUT': params['OUTPUT_C04']
        }
        outputs['C04ProximidadARedesDeTransporteAlternativo'] = processing.run('SISURBANO:C04 Proximidad a redes de transporte alternativo', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['OUTPUT_C04'] = outputs['C04ProximidadARedesDeTransporteAlternativo']['OUTPUT']                    
                          

        # C08 Espacio público ocupado por vehículos parqueados
        steps = steps+1
        feedback.setCurrentStep(steps)  
        if feedback.isCanceled():
            return {}          
        alg_params = {
            'AREA_PER_PARKING': params['AREA_PER_PARKING'],
            'PARKING': params['PARKING'],
            'ROADS': params['ROADS'],
            'STUDY_AREA_GRID': params['STUDY_AREA_GRID'],
            'OUTPUT': params['OUTPUT_C08']
        }
        outputs['C08EspacioPblicoOcupadoPorVehculosParqueados'] = processing.run('SISURBANO:C08 Espacio público ocupado por vehículos parqueados', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['OUTPUT_C08'] = outputs['C08EspacioPblicoOcupadoPorVehculosParqueados']['OUTPUT']

        # C13 Cobertura del servicio de alcantarillado
        steps = steps+1
        feedback.setCurrentStep(steps)  
        if feedback.isCanceled():
            return {}          
        alg_params = {
            'BLOCKS': params['BLOCKS'],
            'FIELD_HOUSING': params['FIELD_HOUSING'],
            'SEWERAGE': params['SEWERAGE'],
            'STUDY_AREA_GRID': params['STUDY_AREA_GRID'],
            'OUTPUT': params['OUTPUT_C13']
        }
        outputs['C13CoberturaDelSistemaDeServicioDeAlcantarillado'] = processing.run('SISURBANO:C13 Cobertura del servicio de alcantarillado', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['OUTPUT_C13'] = outputs['C13CoberturaDelSistemaDeServicioDeAlcantarillado']['OUTPUT']


        return results


    def icon(self):
        return QIcon(os.path.join(pluginPath, 'sisurbano', 'icons', 'make-hexa_logo.png'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'C00 Todos los indicadores C'

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
        return 'C Movilidad urbana'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return IC00WrapC()

    def shortHelpString(self):
        return  "<b>Descripción:</b><br>"\
                "<span>Calcula todos los indicadores de Moviidad urbana</span><br>"\