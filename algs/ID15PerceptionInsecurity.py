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
__date__ = '2020-01-23'
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
                       QgsProcessingParameterFile,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *
from .ZHelpers import *
import numpy as np
import pandas as pd
import tempfile
import subprocess

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class ID15PerceptionInsecurity(QgsProcessingAlgorithm):
    """
    Porcentaje de ciudadanos que se sienten inseguros en su barrio
    Formula:(Población que se siente insegura / Población total)*100
    """

    BLOCKS = 'BLOCKS'
    DPA_SECTOR = 'DPA_SECTOR'
    ENCUESTA = 'ENCUESTA'
    CELL_SIZE = 'CELL_SIZE'
    OUTPUT = 'OUTPUT'
    STUDY_AREA_GRID = 'STUDY_AREA_GRID'
    CURRENT_PATH = 'CURRENT_PATH'    

    def initAlgorithm(self, config):
        currentPath = getCurrentPath(self)
        self.CURRENT_PATH = currentPath        
        FULL_PATH = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID15'][1]))

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BLOCKS,
                self.tr('Zonas Censales'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.DPA_SECTOR,
                self.tr('DPA Zona'),
                'dpa_zona', 'BLOCKS'
            )
        )           


        self.addParameter(
            QgsProcessingParameterFile(
                self.ENCUESTA,
                self.tr('Censo vivienda'),
                extension='csv',
                defaultValue='/Users/terra/llactalab/data/SHAPES_PARA_INDICADORES/victimizacion_personas.csv'
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
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Salida'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH)
            )
        )
        

    def processAlgorithm(self, params, context, feedback):
        steps = 0
        totalStpes = 17
        fieldDpa = params['DPA_SECTOR']
        # fieldHab = params['NUMBER_HABITANTS']

        feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)

        if not OPTIONAL_GRID_INPUT: params['CELL_SIZE'] = P_CELL_SIZE
        grid, isStudyArea = buildStudyArea(params['CELL_SIZE'], params['BLOCKS'],
                                         params['STUDY_AREA_GRID'],
                                         context, feedback)
        gridNeto = grid  


        steps = steps+1
        feedback.setCurrentStep(steps)

        path = params['ENCUESTA']

        file = path

        cols = ['CIUDAD', 'ZONA', 'SECTOR', 'VIVIENDA', 'HOGAR', 'I52']
        df = pd.read_csv(file, usecols=cols)


        # fix codes 
        df['CIUDAD'] = df['CIUDAD'].astype(str)
        df['ZONA'] = df['ZONA'].astype(str)
        df['SECTOR'] = df['SECTOR'].astype(str)
        df['VIVIENDA'] = df['VIVIENDA'].astype(str)
        df['HOGAR'] = df['HOGAR'].astype(str)


        df.loc[df['CIUDAD'].str.len() == 5, 'CIUDAD'] = "0" + df['CIUDAD']
        df.loc[df['ZONA'].str.len() == 1, 'ZONA'] = "00" + df['ZONA']
        df.loc[df['ZONA'].str.len() == 2, 'ZONA'] = "0" + df['ZONA']
        df.loc[df['SECTOR'].str.len() == 1, 'SECTOR'] = "00" + df['SECTOR']
        df.loc[df['SECTOR'].str.len() == 2, 'SECTOR'] = "0" + df['SECTOR']
        df.loc[df['VIVIENDA'].str.len() == 1, 'VIVIENDA'] = "0" + df['VIVIENDA']

        # I52, categorías 1 y 2 (muy inseguro e inseguro)

        df['pobinse'] = 0.0
        df.loc[(df['I52'] == 'Inseguro') | (df['I52'] == 'Muy inseguro'), 'pobinse'] = 1.0

        # codigo sector
        df['codsec'] = df['CIUDAD'].astype(str) + df['ZONA'].astype(str) + df['SECTOR'].astype(str) 
        df['codzon'] = df['CIUDAD'].astype(str) + df['ZONA'].astype(str)

        df.rename(columns={'CIUDAD':'pbt'}, inplace=True) 
        aggOptions = {
                      'codzon' : 'first',
                      'pbt' : 'count',
                      'pobinse' : 'sum',
                     } 

        resManzanas = df.groupby('codzon').agg(aggOptions)
        resManzanas['percepcionins'] = None
        resManzanas['percepcionins'] = (resManzanas['pobinse'] / resManzanas['pbt']) * 100   

        df = resManzanas   

                  
        steps = steps+1
        feedback.setCurrentStep(steps)

        outputCsv = self.CURRENT_PATH+'/percepcionins.csv'
        feedback.pushConsoleInfo(str(('percepcionins en ' + outputCsv)))    
        df.to_csv(outputCsv, index=False)

        steps = steps+1
        feedback.setCurrentStep(steps)

        exitCsv = os.path.exists(outputCsv)
        if(exitCsv):
            print("El archivo CSV existe")
        else:
            print("No se encuentra CSV")

        CSV =  QgsVectorLayer(outputCsv, "csv", "ogr") 
        featuresCSV = CSV.getFeatures()
        # fields = layer.dataProvider().fields()
        field_names = [field.name() for field in CSV.fields()]       
        print(field_names)            


        steps = steps+1
        feedback.setCurrentStep(steps)
        result = joinByAttr2(params['BLOCKS'], fieldDpa,
                                outputCsv, 'codzon',
                                [],
                                UNDISCARD_NONMATCHING,
                                '',
                                1,
                                context,
                                feedback)

        # steps = steps+1
        # feedback.setCurrentStep(steps)
        # expressionNotNull = "percepcionins IS NOT '' AND percepcionins is NOT NULL"    
        # result =   filterByExpression(result['OUTPUT'], expressionNotNull, context, feedback) 



  # ----------------------CONVERTIR A NUMERICOS --------------------     
  
        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaDummy = 'pobinse * 1.0'
        result = calculateField(result['OUTPUT'], 
                                 'pobinse_n',
                                 formulaDummy,
                                 context,
                                 feedback)  

        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaDummy = 'pbt * 1.0'
        result = calculateField(result['OUTPUT'], 
                                 'pbt_n',
                                 formulaDummy,
                                 context,
                                 feedback)    

       # ----------------------PROPORCIONES AREA--------------------------
       
        steps = steps+1
        feedback.setCurrentStep(steps)        
        blocks = calculateArea(result['OUTPUT'], 'area_bloc', context,
                               feedback)     

        steps = steps+1
        feedback.setCurrentStep(steps)
        segments = intersection(blocks['OUTPUT'], gridNeto['OUTPUT'],
                                ['pobinse_n','pbt_n','area_bloc'],
                                ['id_grid','area_grid'],
                                context, feedback)        

        steps = steps+1
        feedback.setCurrentStep(steps)
        segmentsArea = calculateArea(segments['OUTPUT'],
                                     'area_seg',
                                     context, feedback)

        # -------------------------PROPORCIONES VALORES-------------------------

        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaDummy = '(area_seg/area_bloc) * pobinse_n' 
        result = calculateField(segmentsArea['OUTPUT'], 'pobinse_n_seg',
                                               formulaDummy,
                                               context,
                                               feedback)     

        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaDummy = '(area_seg/area_bloc) * pbt_n' 
        result = calculateField(result['OUTPUT'], 'pbt_n_seg',
                               formulaDummy,
                               context,
                               feedback)   


        steps = steps+1
        feedback.setCurrentStep(steps)
        result = makeSureInside(result['OUTPUT'],
                                context,
                                feedback)                                    

        #----------------------------------------------------------------------   

        steps = steps+1
        feedback.setCurrentStep(steps)
        result = joinByLocation(gridNeto['OUTPUT'],
                             result['OUTPUT'],
                             ['pobinse_n_seg','pbt_n_seg'],                                   
                              [CONTIENE], [SUM],
                              UNDISCARD_NONMATCHING,
                              context,
                              feedback)  


        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaDummy = '(pobinse_n_seg_sum/pbt_n_seg_sum) * 100' 
        result = calculateField(result['OUTPUT'], NAMES_INDEX['ID15'][0],
                               formulaDummy,
                               context,
                               feedback, params['OUTPUT'])    


 
        # steps = steps+1
        # feedback.setCurrentStep(steps)
        # gridNeto = joinByLocation(gridNeto['OUTPUT'],
        #                      result['OUTPUT'],
        #                      ['pobinse_viv_n'],                                   
        #                       [INTERSECTA], [MEDIA],
        #                       UNDISCARD_NONMATCHING,
        #                       context,
        #                       feedback)         
 

        # fieldsMapping = [
        #     {'expression': '"id_grid"', 'length': 10, 'name': 'id_grid', 'precision': 0, 'type': 4}, 
        #     {'expression': '"area_grid"', 'length': 16, 'name': 'area_grid', 'precision': 3, 'type': 6}, 
        #     {'expression': '"tenencia_viv_n_mean"', 'length': 20, 'name': NAMES_INDEX['ID15'][0], 'precision': 2, 'type': 6}
        # ]      
        
        # steps = steps+1
        # feedback.setCurrentStep(steps)
        # result = refactorFields(fieldsMapping, gridNeto['OUTPUT'], 
        #                         context,
        #                         feedback, params['OUTPUT'])                                                                

        return result
          
    def icon(self):
        return QIcon(os.path.join(pluginPath, 'sisurbano', 'icons', 'inseguridad.png'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'D15 Percepción de inseguridad'

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
        return ID15PerceptionInsecurity()

    def shortHelpString(self):
        return  "<b>Descripción:</b><br/>"\
                "<span>Porcentaje de ciudadanos que se sienten inseguros en su barrio.</span>"\
                "<br/><br/><b>Justificación y metodología:</b><br/>"\
                "<span>Encuesta de Victimización y Percepción de Inseguridad, 2011. I52, categorías 1 y 2 (muy inseguro e inseguro)</span>"\
                "<br/><br/><b>Formula:</b><br/>"\
                "<span>(Población que se siente insegura / Población total)*100</span><br/>"         
