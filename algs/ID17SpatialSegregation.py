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
from qgis.PyQt.QtGui import QColor
from qgis.core import (QgsProcessing,
                       QgsProcessingMultiStepFeedback,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingUtils,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *
from .ZHelpers import *
import numpy as np
import pandas as pd
import tempfile
import subprocess
import inspect

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class ID17SpatialSegregation(QgsProcessingAlgorithm):
    """
    Mide el cuartil uno de la población en términos de menores recursos,
    respecto al total de la población para el área de estudio. Se utiliza
    el Índice de Segregación Espacial Areal (ISEA). 

    Los cuartiles de la población se obtienen a partir de los índices de vida,
    escogiendo el uno que representa el sector poblacional con mayor carencia.
    Se calcula el ISEA para cada área de estudio. Los sectores de donde la proporción
    de un grupo poblacional es mayor a la población total se indican por valores
    mayores a 1; evidenciando un proceso de segregación. No así si los
    valores son cercanos a 1.    
    Formula: (Porcentaje de la población del Cuartil uno en el Secto i / Porcentaje de la población del Cuartil en toda la ciudad)*100
    """

    ICV = 'ICV'
    OUTPUT = 'OUTPUT'
    FINAL_NAME = None
    VALUE = 'VALUE'
    PT = 'PT'

    def initAlgorithm(self, config):
        currentPath = getCurrentPath(self)
        FULL_PATH = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['ID17'][1]))        

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ICV,
                self.tr('Índice de calidad de vida D07'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.VALUE,
                self.tr('Variable'),
                'PQ1', 'ICV'
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
        totalStpes = 5
        feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)

        p = str(params['VALUE'])

        if p == 'PQ1' or p == 'PQ2' or p == 'PQ3' or p == 'PQ4' or p == 'Pc' or p == 'Po':
            self.PT = str('Pt')
        elif p == 'VQ1' or p == 'VQ2' or p == 'VQ3' or p == 'VQ4' or p == 'Vc' or p == 'Vo':
            self.PT = str('Vt')
        else:
            self.PT = str('0')

        pt = self.PT    

        print("El valor para " + p + " para pt es " + str(pt))    

        steps = steps+1
        feedback.setCurrentStep(steps)
        pp = '('+ p +' * 100) / sum('+ p +')' 
        result = calculateField(params['ICV'] , 'pp',
                                pp,
                                context,
                                feedback)  

        steps = steps+1
        feedback.setCurrentStep(steps)
        ppt = '('+ pt + ' * 100) / sum('+ pt +')' 
        result = calculateField(result['OUTPUT'] , 'ppt',
                                ppt,
                                context,
                                feedback)                                                                        
        
        steps = steps+1
        feedback.setCurrentStep(steps)
        iseg = 'sum(abs('+ pp + ' - '+ ppt + ')) * 0.5' 
        result = calculateField(result['OUTPUT'] , 'ISEG',
                                iseg,
                                context,
                                feedback)   
       
        steps = steps+1
        feedback.setCurrentStep(steps)
        isea = 'pp / ppt' 
        result = calculateField(result['OUTPUT'] , 'ISEA',
                                isea,
                                context,
                                feedback)   

        steps = steps+1
        feedback.setCurrentStep(steps)
        index = 'isea * 1.0' 
        result = calculateField(result['OUTPUT'] , NAMES_INDEX['ID17'][0],
                                index,
                                context,
                                feedback, params['OUTPUT'])           

       
        self.FINAL_NAME = result['OUTPUT']

        return result

       

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'sisurbano', 'icons', 'segregacion.jpg'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'D17 Segregación espacial'

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
        return ID17SpatialSegregation()

    def shortHelpString(self):
        return  "<b>Descripción:</b><br/>"\
                "<span>Haciendo uso del Índice de Segregación de Espacial Local (ISEA), se mide el nivel de exclusión, cohesión o segregación de la población con mayores carencias (cuartil uno según su ICV).</span>"\
                "<br/><br/><b>Justificación y metodología:</b><br/>"\
                "<span>Se utiliza metodología desarrollada por Osorio y Orellana (2014) para la ciudad de Cuenca. Los cuartiles de la población se obtienen a partir de los índices de vida, escogiendo el uno que representa el sector poblacional con mayor carencia. Se calcula el ISEA para cada área de estudio.</span>"\
                "<br/><br/><b>Formula:</b><br/>"\
                "<span>ISEA del Q1 según su ICV<br/>"  

    def postProcessAlgorithm(self, context, feedback):
            cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
            print(cmd_folder)
            segments_score_prop_layer = QgsProcessingUtils.mapLayerFromString(self.FINAL_NAME, context)
            segments_score_prop_layer.renderer().symbol().setColor(QColor("green"))
            # segments_score_prop_layer.loadNamedStyle(os.path.join(os.path.join(cmd_folder, 'style.qml')))
            # segments_score_prop_layer.renderer().updateClasses(segments_score_prop_layer, segments_score_prop_layer.renderer().EqualInterval, 8)            
            segments_score_prop_layer.triggerRepaint()
            # Do smth with the layer, e.g. style it
            return {
                     "OUTPUT" : self.FINAL_NAME
                   }        
