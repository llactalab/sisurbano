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
__date__ = '2019-10-13'
__copyright__ = '(C) 2019 by LlactaLAB'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing,
                       QgsProcessingMultiStepFeedback,
                       QgsFeatureSink,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterEnum,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *
from .ZHelpers import *

#pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class ID00WrapD(QgsProcessingAlgorithm):
    """
    Calcula todos los indicadores de ambiente construido
    """


    BLOCKS = 'BLOCKS'
    FIELD_POPULATION = 'FIELD_POPULATION'
    FIELD_HOUSING = 'FIELD_HOUSING'    
    CELL_SIZE = 'CELL_SIZE'
    STUDY_AREA_GRID = 'STUDY_AREA_GRID'
    DISTANCE_OPTIONS = 'DISTANCE_OPTIONS'    

    #-----------------D01----------------------  
    DPA_MAN = 'DPA_MAN'
    CENSO_VIVIENDA = 'CENSO_VIVIENDA'
    #-----------------D02----------------------    

    #-----------------D03----------------------    
    RISK = 'RISK'
    #-----------------D04----------------------
    OPEN_SPACE = 'OPEN_SPACE'
    SPACE2IMPROVEMENT = 'SPACE2IMPROVEMENT'
    #-----------------D05-----------------------
    CENSO_HOGAR = 'CENSO_HOGAR'    
    #-----------------D06-----------------------
    DPA_SECTOR = 'DPA_SECTOR'
    ENCUESTA_TIEMPO = 'ENCUESTA_TIEMPO'    
    ZONAS_CENSALES = 'ZONAS_CENSALES'
    #-----------------D07-----------------------
    CENSO_POBLACION = 'CENSO_POBLACION'
    #-----------------D08-----------------------
    EQUIPMENT_MARKET = 'EQUIPMENT_MARKET'  
    ROADS = 'ROADS'      
    #-----------------D09---------------------
    THEFTS = 'THEFTS'    
    #-----------------D10--------------------
    #-----------------D11--------------------
    ENCUESTA_DESEMPLEO = 'ENCUESTA_DESEMPLEO'       
    #-----------------D12---------------------
    #-----------------D13-----------------------
    #-----------------D14---------------------
    #-----------------D15-----------------------
    ENCUESTA_SEGURIDAD = 'ENCUESTA_SEGURIDAD'
    #-----------------D16-----------------------
    #-----------------D17-----------------------
    ICV = 'ICV'
    VALUE = 'VALUE'


    #-----------------OUTPUTS----------------------
    OUTPUT_D01 = 'OUTPUT_D01'
    OUTPUT_D02 = 'OUTPUT_D02'
    OUTPUT_D03 = 'OUTPUT_D03'
    OUTPUT_D04 = 'OUTPUT_D04'
    OUTPUT_D05 = 'OUTPUT_D05'
    OUTPUT_D06 = 'OUTPUT_D06'
    OUTPUT_D07 = 'OUTPUT_D07'
    OUTPUT_D08 = 'OUTPUT_D08'
    OUTPUT_D09 = 'OUTPUT_D09'
    OUTPUT_D10 = 'OUTPUT_D10'
    OUTPUT_D11 = 'OUTPUT_D11'
    OUTPUT_D12 = 'OUTPUT_D12'
    OUTPUT_D13 = 'OUTPUT_D13'
    OUTPUT_D14 = 'OUTPUT_D14'
    OUTPUT_D15 = 'OUTPUT_D15'
    OUTPUT_D16 = 'OUTPUT_D16'
    OUTPUT_D17 = 'OUTPUT_D17'


    def initAlgorithm(self, config):

        currentPath = getCurrentPath(self)
        FULL_PATH_D01 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID01'][1]))
        FULL_PATH_D02 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID02'][1]))
        FULL_PATH_D03 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID03'][1]))
        FULL_PATH_D04 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID04'][1]))
        FULL_PATH_D05 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID05'][1]))
        FULL_PATH_D06 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID06'][1]))
        FULL_PATH_D07 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID07'][1]))
        FULL_PATH_D08 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID08'][1]))
        FULL_PATH_D09 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID09'][1]))
        FULL_PATH_D10 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID10'][1]))
        FULL_PATH_D11 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID11'][1]))
        FULL_PATH_D12 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID12'][1]))
        FULL_PATH_D13 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID13'][1]))
        FULL_PATH_D14 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID14'][1]))
        FULL_PATH_D15 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID15'][1]))
        FULL_PATH_D16 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID16'][1]))
        FULL_PATH_D17 = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID17'][1]))



        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.STUDY_AREA_GRID,
                self.tr(TEXT_GRID_INPUT),
                [QgsProcessing.TypeVectorPolygon],
                '', OPTIONAL_GRID_INPUT
            )
        )

        #-----------------D01----------------------  
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
                self.FIELD_POPULATION,
                self.tr('Población'),
                'poblacion', 'BLOCKS'
            )
        )        
        
        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD_HOUSING,
                self.tr('Viviendas'),
                'viviendas', 'BLOCKS',
                optional = True,
            )
        )             

        self.addParameter(
            QgsProcessingParameterField(
                self.DPA_MAN,
                self.tr('DPA Manzanas'),
                'dpa_manzan', 'BLOCKS'
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

        #-----------------D02----------------------    
 
        #-----------------D03----------------------    
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.RISK,
                self.tr('Zonas de riesgo'),
                [QgsProcessing.TypeVectorAnyGeometry],
                optional = True,
                defaultValue=""
            )
        )
        #-----------------D04----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.OPEN_SPACE,
                self.tr('Espacios públicos abiertos'),
                [QgsProcessing.TypeVectorAnyGeometry],
                optional = True,
                defaultValue=""                
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.SPACE2IMPROVEMENT,
                self.tr('Espacios públicos abiertos que necesitan mejoras'),
                [QgsProcessing.TypeVectorAnyGeometry],
                optional = True,
                defaultValue=""                
            )
        )

        #-----------------D05----------------------
        self.addParameter(
            QgsProcessingParameterFile(
                self.CENSO_HOGAR,
                self.tr('Censo hogar'),
                extension='csv',
                defaultValue="",
                optional = True           
            )
        )                        
        #-----------------D06----------------------

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ZONAS_CENSALES,
                self.tr('Zonas Censales'),
                [QgsProcessing.TypeVectorPolygon],
                optional = True,
                defaultValue=""                
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.DPA_SECTOR,
                self.tr('DPA Zona'),
                'dpa_zona', 'ZONAS_CENSALES',
                optional = True            
            )
        )           

        self.addParameter(
            QgsProcessingParameterFile(
                self.ENCUESTA_TIEMPO,
                self.tr('Encuesta específica de uso del tiempo'),
                extension='csv',
                defaultValue='',
                optional = True            
            )
        )           

        #-----------------D07----------------------
        self.addParameter(
            QgsProcessingParameterFile(
                self.CENSO_POBLACION,
                self.tr('Censo población'),
                extension='csv',
                defaultValue="",
                optional = True              
            )
        ) 
        #-----------------D08----------------------
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
                self.EQUIPMENT_MARKET,
                self.tr('Mercados públicos'),
                [QgsProcessing.TypeVectorPoint],
                optional = True,
                defaultValue=""                
            )
        )        
        #-----------------D09----------------------
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.THEFTS,
                self.tr('Robos'),
                [QgsProcessing.TypeVectorPoint],
                optional = True,
                defaultValue=""                
            )
        )

        #-----------------D10----------------------
        #-----------------D11----------------------

        self.addParameter(
            QgsProcessingParameterFile(
                self.ENCUESTA_DESEMPLEO,
                self.tr('Encuesta de Empleo, Desempleo y Subempleo'),
                extension='csv',
                defaultValue='',
                optional = True             
            )
        )           

        # ------------------D12------------------------
        # ------------------D13------------------------
        # ------------------D14------------------------
        # ------------------D15------------------------
        self.addParameter(
            QgsProcessingParameterFile(
                self.ENCUESTA_SEGURIDAD,
                self.tr('Encuesta de victimización y percepción de inseguridad'),
                extension='csv',
                defaultValue='',
                optional = True            
            )
        )          
        # ------------------D16------------------------
        # ------------------D17------------------------

        # self.addParameter(
        #     QgsProcessingParameterFeatureSource(
        #         self.ICV,
        #         self.tr('Índice de calidad de vida D07'),
        #         [QgsProcessing.TypeVectorPolygon],
        #         optional = True,
        #         defaultValue=""                
        #     )
        # )

        # self.addParameter(
        #     QgsProcessingParameterField(
        #         self.VALUE,
        #         self.tr('Variable'),
        #         'PQ1', 'ICV',
        #         optional = True            
        #     )
        # )            
    
        #-----------------OUTPUT----------------------          

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D01,
                self.tr('D01 Viviendas con cobertura total de servicios básicos'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D01)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D02,
                self.tr('D02 Viviendas con carencias constructivas'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D02)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D03,
                self.tr('D03 Viviendas emplazadas en zonas vulnerables y de riesgo'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D03)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D04,
                self.tr('D04 Espacios públicos abiertos que necesitan mejoras'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D04)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D05,
                self.tr('D05 Acceso a internet'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D05)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D06,
                self.tr('D06 Uso del tiempo'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D06)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D07,
                self.tr('D07 Indice de calidad de vida'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D07)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D08,
                self.tr('D08 Cercanía y asequibilidad a alimentos'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D08)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D09,
                self.tr('D09 Robos por número de habitantes'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D09)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D10,
                self.tr('D10 Seguridad de tenencia de la vivienda'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D10)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D11,
                self.tr('D11 Tasa de desempleo'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D11)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D12,
                self.tr('D12 Mujeres en la fuerza de trabajo remunerado'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D12)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D13,
                self.tr('D13 Población activa con estudios universitarios'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D13)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D14,
                self.tr('D14 Estabilidad de la comunidad'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D14)
            )
        )            

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D15,
                self.tr('D15 Percepción de inseguridad'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D15)
            )
        )     


        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D16,
                self.tr('D16 Índice de envejecimiento'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D16)
            )
        )     

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_D17,
                self.tr('D17 Segregación Espacial'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH_D17)
            )
        )     



    def processAlgorithm(self, parameters, context, feedback):
        steps = 0
        totalStpes = 17
        outputs = {}
        results = {}
        feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)

        isValid = lambda x: False if x is None or x is '' else True

        isBlocks = isValid(parameters['BLOCKS'])        
        isFieldPopulation = isValid(parameters['FIELD_POPULATION'])
        isFieldHousing = isValid(parameters['FIELD_HOUSING'])
        isStudyArea = isValid(parameters['STUDY_AREA_GRID']) 



        # isIcv = isValid(parameters['ICV'])
        # isValue = isValid(parameters['VALUE'])


        isCensoVivienda = isValid(parameters['CENSO_VIVIENDA'])            
        isDpaMan = isValid(parameters['DPA_MAN'])            

        print("Censo Vivienda")
        print(isCensoVivienda)

        if isBlocks and isCensoVivienda and isDpaMan:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D02 Viviendas con carencias constructivas
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'CENSO_VIVIENDA': parameters['CENSO_VIVIENDA'],
                'DPA_MAN': parameters['DPA_MAN'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D02']
            }
            outputs['D02ViviendasConCarenciasConstructivas'] = processing.run('SISURBANO:D02 Viviendas con carencias constructivas', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D02'] = outputs['D02ViviendasConCarenciasConstructivas']['OUTPUT']



        isCensoHogar = isValid(parameters['CENSO_HOGAR']) 


        if isCensoVivienda and isBlocks and isCensoHogar and isDpaMan:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}
            # D05 Acceso a internet
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'CENSO_HOGAR': parameters['CENSO_HOGAR'],
                'CENSO_VIVIENDA': parameters['CENSO_VIVIENDA'],
                'DPA_MAN':   parameters['DPA_MAN'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D05']
            }
            outputs['D05AccesoAInternet'] = processing.run('SISURBANO:D05 Acceso a internet', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D05'] = outputs['D05AccesoAInternet']['OUTPUT']


        isThefts = isValid(parameters['THEFTS']) 


        if isBlocks and isFieldPopulation and isThefts:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D09 Número de robos anuales
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'FIELD_POPULATION':  parameters['FIELD_POPULATION'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'THEFTS': parameters['THEFTS'],
                'OUTPUT': parameters['OUTPUT_D09']
            }
            outputs['D09NmeroDeRobosAnuales'] = processing.run('SISURBANO:D09 Número de robos anuales', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D09'] = outputs['D09NmeroDeRobosAnuales']['OUTPUT']


        isCensoPoblacion = isValid(parameters['CENSO_POBLACION']) 

        if isBlocks and isCensoPoblacion and isDpaMan:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D13 Población activa con estudios universitarios
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'CENSO_POBLACION': parameters['CENSO_POBLACION'],
                'DPA_MAN':  parameters['DPA_MAN'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D13']
            }
            outputs['D13PoblacinActivaConEstudiosUniversitarios'] = processing.run('SISURBANO:D13 Población activa con estudios universitarios', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D13'] = outputs['D13PoblacinActivaConEstudiosUniversitarios']['OUTPUT']



        if isBlocks and isCensoVivienda and isDpaMan:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D01 Viviendas con cobertura total de servicios básicos
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'CENSO_VIVIENDA': parameters['CENSO_VIVIENDA'],
                'DPA_MAN': parameters['DPA_MAN'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D01']
            }
            outputs['D01ViviendasConCoberturaTotalDeServiciosBsicos'] = processing.run('SISURBANO:D01 Viviendas con cobertura total de servicios básicos', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D01'] = outputs['D01ViviendasConCoberturaTotalDeServiciosBsicos']['OUTPUT']


        isDistanceOptions = isValid(parameters['DISTANCE_OPTIONS']) 
        isMarket = isValid(parameters['EQUIPMENT_MARKET']) 
        isRoads =  isValid(parameters['ROADS']) 

        if isBlocks and isDistanceOptions and isMarket and isRoads:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D08 Cercanía y asequibilidad a alimentos
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'DISTANCE_OPTIONS': parameters['DISTANCE_OPTIONS'],
                'EQUIPMENT_MARKET': parameters['EQUIPMENT_MARKET'],
                'FIELD_HOUSING': parameters['FIELD_HOUSING'],
                'ROADS': parameters['ROADS'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D08']
            }
            outputs['D08CercanaYAsequibilidadAAlimentos'] = processing.run('SISURBANO:D08 Cercanía y asequibilidad a alimentos', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D08'] = outputs['D08CercanaYAsequibilidadAAlimentos']['OUTPUT']


        isZonasCensales =  isValid(parameters['ZONAS_CENSALES']) 
        isEncuestaTiempo =  isValid(parameters['ENCUESTA_TIEMPO']) 
        isDpaSector =  isValid(parameters['DPA_SECTOR']) 

        
        if isZonasCensales and isDpaSector and isEncuestaTiempo:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D06 Uso del tiempo
            alg_params = {
                'BLOCKS': parameters['ZONAS_CENSALES'],
                'DPA_SECTOR': parameters['DPA_SECTOR'],
                'ENCUESTA': parameters['ENCUESTA_TIEMPO'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D06']
            }
            outputs['D06UsoDelTiempo'] = processing.run('SISURBANO:D06 Uso del tiempo', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D06'] = outputs['D06UsoDelTiempo']['OUTPUT']


        isEncuestaSeguridad =  isValid(parameters['ENCUESTA_SEGURIDAD']) 

        if isZonasCensales and isDpaSector and isEncuestaSeguridad:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D15 Percepción de inseguridad
            alg_params = {
                'BLOCKS': parameters['ZONAS_CENSALES'],
                'DPA_SECTOR': parameters['DPA_SECTOR'],
                'ENCUESTA': parameters['ENCUESTA_SEGURIDAD'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D15']
            }
            outputs['D15PercepcinDeInseguridad'] = processing.run('SISURBANO:D15 Percepción de inseguridad', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D15'] = outputs['D15PercepcinDeInseguridad']['OUTPUT']


        if isBlocks and isCensoPoblacion and isDpaMan:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D16 Índice de envejecimiento
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'CENSO_POBLACION': parameters['CENSO_POBLACION'],
                'DPA_MAN': parameters['DPA_MAN'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D16']
            }
            outputs['D16NdiceDeEnvejecimiento'] = processing.run('SISURBANO:D16 Índice de envejecimiento', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D16'] = outputs['D16NdiceDeEnvejecimiento']['OUTPUT']


        isEncuestaDesempleo =  isValid(parameters['ENCUESTA_DESEMPLEO']) 

        if isZonasCensales and isDpaSector and isEncuestaDesempleo:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D11 Tasa de desempleo
            alg_params = {
                'BLOCKS': parameters['ZONAS_CENSALES'],
                'DPA_SECTOR': parameters['DPA_SECTOR'],
                'ENCUESTA': parameters['ENCUESTA_DESEMPLEO'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D11']
            }
            outputs['D11TasaDeDesempleo'] = processing.run('SISURBANO:D11 Tasa de desempleo', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D11'] = outputs['D11TasaDeDesempleo']['OUTPUT']


        isOpenSpace =  isValid(parameters['OPEN_SPACE']) 
        isSpace2Improvement =  isValid(parameters['SPACE2IMPROVEMENT']) 



        if isOpenSpace and isSpace2Improvement:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D04 Espacios públicos abiertos que necesitan mejoras
            alg_params = {
                'OPEN_SPACE': parameters['OPEN_SPACE'],
                'SPACE2IMPROVEMENT': parameters['SPACE2IMPROVEMENT'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D04']
            }
            outputs['D04EspaciosPblicosAbiertosQueNecesitanMejoras'] = processing.run('SISURBANO:D04 Espacios públicos abiertos que necesitan mejoras', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D04'] = outputs['D04EspaciosPblicosAbiertosQueNecesitanMejoras']['OUTPUT']



        if isBlocks and isCensoPoblacion and isDpaMan:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D12 Mujeres en la fuerza de trabajo remunerado
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'CENSO_POBLACION': parameters['CENSO_POBLACION'],
                'DPA_MAN': parameters['DPA_MAN'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D12']
            }
            outputs['D12MujeresEnLaFuerzaDeTrabajoRemunerado'] = processing.run('SISURBANO:D12 Mujeres en la fuerza de trabajo remunerado', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D12'] = outputs['D12MujeresEnLaFuerzaDeTrabajoRemunerado']['OUTPUT']

        isRisk =  isValid(parameters['RISK']) 
        if isBlocks and isFieldHousing and isRisk:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D03 Viviendas emplazadas en zonas de riesgo
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'FIELD_HOUSING':  parameters['FIELD_HOUSING'],
                'RISK': parameters['RISK'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D03']
            }
            outputs['D03ViviendasEmplazadasEnZonasDeRiesgo'] = processing.run('SISURBANO:D03 Viviendas emplazadas en zonas de riesgo', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D03'] = outputs['D03ViviendasEmplazadasEnZonasDeRiesgo']['OUTPUT']


        if isBlocks and isCensoHogar and isCensoVivienda and isDpaMan:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D10 Seguridad de tenencia de la vivienda
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'CENSO_HOGAR': parameters['CENSO_HOGAR'],
                'CENSO_VIVIENDA': parameters['CENSO_VIVIENDA'],
                'DPA_MAN':  parameters['DPA_MAN'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D10']
            }
            outputs['D10SeguridadDeTenenciaDeLaVivienda'] = processing.run('SISURBANO:D10 Seguridad de tenencia de la vivienda', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D10'] = outputs['D10SeguridadDeTenenciaDeLaVivienda']['OUTPUT']


        if isBlocks and isCensoPoblacion and isDpaMan:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D14 Estabilidad de la comunidad
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'CENSO_POBLACION': parameters['CENSO_POBLACION'],
                'DPA_MAN': parameters['DPA_MAN'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D14']
            }
            outputs['D14EstabilidadDeLaComunidad'] = processing.run('SISURBANO:D14 Estabilidad de la comunidad', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D14'] = outputs['D14EstabilidadDeLaComunidad']['OUTPUT']


        if isBlocks and isCensoHogar and isCensoPoblacion and isCensoVivienda and isDpaMan:
            steps = steps+1
            feedback.setCurrentStep(steps)  
            if feedback.isCanceled():
                return {}

            # D07 Indice de calidad de vida
            alg_params = {
                'BLOCKS': parameters['BLOCKS'],
                'CENSO_HOGAR': parameters['CENSO_HOGAR'],
                'CENSO_POBLACION': parameters['CENSO_POBLACION'],
                'CENSO_VIVIENDA': parameters['CENSO_VIVIENDA'],
                'DPA_MAN':  parameters['DPA_MAN'],
                'STUDY_AREA_GRID': parameters['STUDY_AREA_GRID'],
                'OUTPUT': parameters['OUTPUT_D07']
            }
            outputs['D07IndiceDeCalidadDeVida'] = processing.run('SISURBANO:D07 Indice de calidad de vida', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D07'] = outputs['D07IndiceDeCalidadDeVida']['OUTPUT']      
        

        if results['OUTPUT_D07']:
            # D17 Segregación espacial
            alg_params = {
                'ICV': results['OUTPUT_D07'],
                'VALUE': 'PQ1',
                'OUTPUT': parameters['OUTPUT_D17']
            }
            outputs['D17SegregacinEspacial'] = processing.run('SISURBANO:D17 Segregación espacial', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['OUTPUT_D17'] = outputs['D17SegregacinEspacial']['OUTPUT']            
                    

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
        return 'D00 Todos los indicadores D'

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
        return 'D Dinámicas socio-espaciales'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ID00WrapD()

    def shortHelpString(self):
        return  "<b>Descripción:</b><br/>"\
                "<span>Calcula todos los indicadores de Dinámicas socio-espaciales</span>"