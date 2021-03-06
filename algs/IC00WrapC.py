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
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFile,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *
from .ZHelpers import *

#pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

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
    DISTANCE_OPTIONS = 'DISTANCE_OPTIONS'
    ROADS = 'ROADS'        
    BUSSTOP = 'BUSSTOP'    
    TRAMSTOP = 'TRAMSTOP'    
    BIKESTOP = 'BIKESTOP'    
    BIKEWAY = 'BIKEWAY'    
    CROSSWALK = 'CROSSWALK'
    #-----------------C05----------------------
    PARKING = 'PARKING'
    AREA_PER_PARKING = 'AREA_PER_PARKING'
    DPA_MAN = 'DPA_MAN'
    #-----------------C09------------------------
    CENSO_VIVIENDA = 'CENSO_VIVIENDA'
    CENSO_HOGAR = 'CENSO_HOGAR'    
    #-----------------C13----------------------
    SEWERAGE = 'SEWERAGE'
    #-----------------OUTPUTS----------------------
    OUTPUT_C01 = 'OUTPUT_C01'
    OUTPUT_C03 = 'OUTPUT_C03'
    OUTPUT_C04 = 'OUTPUT_C04'
    OUTPUT_C05 = 'OUTPUT_C05'
    OUTPUT_C09 = 'OUTPUT_C09'
    OUTPUT_C13 = 'OUTPUT_C13'


    def initAlgorithm(self, config):

        currentPath = getCurrentPath(self)
        FULL_PATH_C01 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC01'][1]))
        FULL_PATH_C03 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC03'][1]))
        FULL_PATH_C04 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC04'][1]))
        FULL_PATH_C05 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC05'][1]))
        FULL_PATH_C09 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC09'][1]))
        FULL_PATH_C13 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC13'][1]))


    #-----------------OTHERS----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.STUDY_AREA_GRID,
                self.tr(TEXT_GRID_INPUT),
                [QgsProcessing.TypeVectorPolygon],
                '', OPTIONAL_GRID_INPUT
            )
        )


        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BLOCKS,
                self.tr('Manzanas'),
                [QgsProcessing.TypeVectorPolygon],
                optional = True,
                defaultValue=""
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.DPA_MAN,
                self.tr('DPA Manzanas'),
                'dpa_manzan', 'BLOCKS',
                 optional = True
            )
        )           

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD_POPULATION,
                self.tr('Población'),
                'poblacion', 'BLOCKS',
                optional = True
            )
        )  

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD_HOUSING,
                self.tr('Viviendas'),
                'viviendas', 'BLOCKS',
                optional = True
            )
        )   

    #-----------------C01----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ROADS,
                self.tr('Viario público'),
                [QgsProcessing.TypeVectorPolygon],
                optional = True,
                defaultValue=""
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.WALK_ROAD,
                self.tr('Viario público peatonal'),
                [QgsProcessing.TypeVectorPolygon],
                optional = True,
                defaultValue=""
            )
        )    
    #-----------------C03----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ROADS_LINES,
                self.tr('Vías públicas'),
                [QgsProcessing.TypeVectorLine],
                optional = True,
                defaultValue=""
            )
        )
    #-----------------C04----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ROADS,
                self.tr('Red vial'),
                [QgsProcessing.TypeVectorLine],
                optional = True,
                defaultValue = ''
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
                self.BUSSTOP,
                self.tr('Paradas de bus'),
                [QgsProcessing.TypeVectorPoint],
                optional = True,
                defaultValue=""
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.TRAMSTOP,
                self.tr('Tranvía'),
                [QgsProcessing.TypeVectorPoint],
                optional = True,
                defaultValue=""
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BIKESTOP,
                self.tr('Bici pública'),
                [QgsProcessing.TypeVectorPoint],
                optional = True,
                defaultValue=""
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BIKEWAY,
                self.tr('Ciclovía'),
                [QgsProcessing.TypeVectorLine],
                optional = True,
                defaultValue=""
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.CROSSWALK,
                self.tr('Caminos peatonales'),
                [QgsProcessing.TypeVectorLine],
                optional = True,
                defaultValue=""
            )
        )                                
    #-----------------C05----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.PARKING,
                self.tr('Puestos de parqueo'),
                [QgsProcessing.TypeVectorPoint],
                optional = True,
                defaultValue=""
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
                [QgsProcessing.TypeVectorAnyGeometry],
                optional = True,
                defaultValue=""
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.CENSO_HOGAR,
                self.tr('Censo hogar'),
                extension='csv',
                defaultValue="",
                optional = True
            )
        )           

        self.addParameter(
            QgsProcessingParameterFile(
                self.CENSO_VIVIENDA,
                self.tr('Censo vivienda'),
                extension='csv',
                defaultValue='',
                optional = True
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
                self.OUTPUT_C05,
                self.tr('C05 Espacio público ocupado por vehículos parqueados'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_C05)
            )
        )  

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_C09,
                self.tr('C09 Consumo de energía eléctrica en la vivienda'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_C09)
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

        isValid = lambda x: False if x is None else True

        isBlocks = isValid(params['BLOCKS'])        
        isFieldPopulation = isValid(params['FIELD_POPULATION'])
        isFieldHousing = isValid(params['FIELD_HOUSING'])
        isStudyArea = isValid(params['STUDY_AREA_GRID']) 

        isRoads = isValid(params['ROADS'])        
        isWalkRoad = isValid(params['WALK_ROAD'])        



        if isRoads and isWalkRoad:
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


        isRoadsLines = isValid(params['ROADS_LINES']) 

        if isBlocks and isFieldPopulation and isRoadsLines:
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


        isBikeStop = isValid(params['BIKESTOP'])
        isBikeWay = isValid(params['BIKEWAY'])
        isBusStop = isValid(params['BUSSTOP'])
        isCrossWalk = isValid(params['CROSSWALK'])
        isDistanceOptions = isValid(params['DISTANCE_OPTIONS'])
        isTramStop = isValid(params['TRAMSTOP'])

        if (isBikeStop and isBikeWay and isBlocks and isBusStop and isCrossWalk and isRoads
            and isDistanceOptions and isFieldPopulation and isTramStop):
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
                'ROADS': params['ROADS'],
                'DISTANCE_OPTIONS': params['DISTANCE_OPTIONS'],               
                'FIELD_POPULATE_HOUSING': params['FIELD_POPULATION'],
                'STUDY_AREA_GRID': params['STUDY_AREA_GRID'],
                'TRAMSTOP': params['TRAMSTOP'],
                'OUTPUT': params['OUTPUT_C04']
            }
            outputs['C04ProximidadARedesDeTransporteAlternativo'] = processing.run('SISURBANO:C04 Proximidad a redes de transporte alternativo', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_C04'] = outputs['C04ProximidadARedesDeTransporteAlternativo']['OUTPUT']                    
                          

        isAreaPerParking = isValid(params['AREA_PER_PARKING'])
        isParking = isValid(params['PARKING'])

        if isAreaPerParking and isParking and isRoads:
            # C05 Espacio público ocupado por vehículos parqueados
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}          
            alg_params = {
                'AREA_PER_PARKING': params['AREA_PER_PARKING'],
                'PARKING': params['PARKING'],
                'ROADS': params['ROADS'],
                'STUDY_AREA_GRID': params['STUDY_AREA_GRID'],
                'OUTPUT': params['OUTPUT_C05']
            }
            outputs['C05EspacioPblicoOcupadoPorVehculosParqueados'] = processing.run('SISURBANO:C05 Espacio público ocupado por vehículos parqueados', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_C05'] = outputs['C05EspacioPblicoOcupadoPorVehculosParqueados']['OUTPUT']

        


        isCensoVivienda = isValid(params['CENSO_VIVIENDA'])
        isCensoHogar = isValid(params['CENSO_HOGAR'])
        isDpaMan = isValid(params['DPA_MAN'])

        if isCensoHogar and isCensoVivienda and isDpaMan:
            # C09 Consumo de energía eléctrica en la vivienda
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}               
            alg_params = {
                'BLOCKS': params['BLOCKS'],
                'CENSO_HOGAR': params['CENSO_HOGAR'],
                'CENSO_VIVIENDA':params['CENSO_VIVIENDA'],
                'DPA_MAN': params['DPA_MAN'],
                'STUDY_AREA_GRID': params['STUDY_AREA_GRID'],
                'OUTPUT': params['OUTPUT_C09'],
            }
            outputs['C09ConsumoDeEnergaElctricaEnLaVivienda'] = processing.run('SISURBANO:C09 Consumo de energía eléctrica en la vivienda', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_C09'] = outputs['C09ConsumoDeEnergaElctricaEnLaVivienda']['OUTPUT']


        isSewerage = isValid(params['SEWERAGE'])

        if isBlocks and isFieldHousing and isSewerage:
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
        return QIcon(os.path.join(pluginPath, 'make-hexa_logo.png'))

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
        return  "<b>Descripción:</b><br/>"\
                "<span>Calcula todos los indicadores de Moviidad urbana</span><br/>"