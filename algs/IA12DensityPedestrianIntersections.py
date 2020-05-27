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
__date__ = '2020-01-27'
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

#pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class IA12DensityPedestrianIntersections(QgsProcessingAlgorithm):
    """
    Mide la conectividad de un territorio para el peatón. Relación entre el
    número de intersecciones de calles e intersecciones peatonales y
    la superficie del área de estudio. 

    1. Obtener el mapa de la red de calles del área urbana. de OSM
    2. Verifique la topología: cada segmento de calle debe estar correctamente conectado a otros segmentos.
    3. Obtener el punto de inicio y final de cada segmento.
    4. Recopile eventos desde los puntos de inicio y finalización: recopile los puntos finales múltiples en una intersección juntos y cuente los números de puntos finales en cada intersección.
    5. Excluya los puntos con menos de 3 eventos, es decir, los callejones sin salida o los extremos de segmentos rotos.
    6. Cuente los puntos restantes y divida por el área de estudio en km2.

    Número de intersecciones / Superficie del área en Km2
    """

    ROADS = 'ROADS'
    # FIELD_SINTAXIS = 'FIELD_SINTAXIS'
    CELL_SIZE = 'CELL_SIZE'
    OUTPUT = 'OUTPUT'
    STUDY_AREA_GRID = 'STUDY_AREA_GRID'


    def initAlgorithm(self, config):

        currentPath = getCurrentPath(self)
        FULL_PATH = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IA12'][1]))

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ROADS,
                self.tr('Vías'),
                [QgsProcessing.TypeVectorLine]
            )
        )

        # self.addParameter(
        #     QgsProcessingParameterField(
        #         self.FIELD_SINTAXIS,
        #         self.tr('Valor'),
        #         'NACH_slen', 'ROADS'
        #     )
        # )        

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
        totalStpes = 10
        # fieldSintaxis = params['FIELD_SINTAXIS']

        feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)


        steps = steps+1
        feedback.setCurrentStep(steps)
        if not OPTIONAL_GRID_INPUT: params['CELL_SIZE'] = P_CELL_SIZE
        grid, isStudyArea = buildStudyArea(params['CELL_SIZE'], params['ROADS'],
                                           params['STUDY_AREA_GRID'],
                                           context, feedback)
        gridNeto = grid

        results = {}
        outputs = {}


        # Dividir con líneas
        alg_params = {
            'INPUT': params['ROADS'],
            'LINES': params['ROADS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DividirConLneas'] = processing.run('native:splitwithlines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'idx',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '$id',
            'INPUT': outputs['DividirConLneas']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampos'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Intersección de lineas
        alg_params = {
            'INPUT': outputs['CalculadoraDeCampos']['OUTPUT'],
            'INPUT_FIELDS': 'idx',
            'INTERSECT': outputs['CalculadoraDeCampos']['OUTPUT'],
            'INTERSECT_FIELDS': 'idx',
            'INTERSECT_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['InterseccinDeLineas'] = processing.run('native:lineintersections', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Disolver
        alg_params = {
            'FIELD': 'idx',
            'INPUT': outputs['InterseccinDeLineas']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Disolver'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Convert multipoints to points
        alg_params = {
            'MULTIPOINTS': outputs['Disolver']['OUTPUT'],
            'POINTS': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ConvertMultipointsToPoints'] = processing.run('saga:convertmultipointstopoints', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Agrupamiento DBSCAN
        alg_params = {
            'DBSCAN*': False,
            'EPS': 0.1,
            'FIELD_NAME': 'CLUSTER_ID',
            'INPUT': outputs['ConvertMultipointsToPoints']['POINTS'],
            'MIN_SIZE': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AgrupamientoDbscan'] = processing.run('native:dbscanclustering', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Disolver last
        alg_params = {
            'FIELD': 'CLUSTER_ID',
            'INPUT': outputs['AgrupamientoDbscan']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DisolverLast'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Unir atributos por localización (resumen)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['DisolverLast']['OUTPUT'],
            'JOIN': outputs['ConvertMultipointsToPoints']['POINTS'],
            'JOIN_FIELDS': 'idx',
            'PREDICATE': [0],
            'SUMMARIES': [0],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirAtributosPorLocalizacinResumen'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Seleccionar por expresión
        alg_params = {
            'EXPRESSION': 'idx_count >=3',
            'INPUT': outputs['UnirAtributosPorLocalizacinResumen']['OUTPUT'],
            'METHOD': 0
        }
        outputs['SeleccionarPorExpresin'] = processing.run('qgis:selectbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Extraer los objetos espaciales seleccionados
        alg_params = {
            'INPUT': outputs['SeleccionarPorExpresin']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraerLosObjetosEspacialesSeleccionados'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


        steps = steps+1
        feedback.setCurrentStep(steps)
        result = joinByLocation(gridNeto['OUTPUT'],
                                 outputs['ExtraerLosObjetosEspacialesSeleccionados']['OUTPUT'],
                                 ['idx_count'],                                   
                                  [CONTIENE], [COUNT],
                                  UNDISCARD_NONMATCHING,
                                  context,
                                  feedback)   

        steps = steps+1
        feedback.setCurrentStep(steps)
        formulaDummy = 'idx_count_count / (area_grid / 1000000)'
        result = calculateField(result['OUTPUT'],
                                   NAMES_INDEX['IA12'][0],
                                   formulaDummy,
                                   context,
                                   feedback, params['OUTPUT'])



        return result



    def icon(self):
        return QIcon(os.path.join(pluginPath, 'densidadinter.png'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'A12 Densidad de intersecciones peatonales'

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
        return IA12DensityPedestrianIntersections()

    def shortHelpString(self):
        return  "<b>Descripción:</b><br/>"\
                "<span>Mide la conectividad de un territorio para el peatón. Relación entre el número de intersecciones de calles e intersecciones peatonales y la superficie del área de estudio. </span>"\
                "<br/><br/><b>Justificación y metodología:</b><br/>"\
                "<span>1. Obtener el mapa de la red de calles del área urbana. de OSM 2. Verifique la topología: cada segmento de calle debe estar correctamente conectado a otros segmentos. 3. Obtener el punto de inicio y final de cada segmento. 4. Recopile eventos desde los puntos de inicio y finalización: recopile los puntos finales múltiples en una intersección juntos y cuente los números de puntos finales en cada intersección. 5. Excluya los puntos con menos de 3 eventos, es decir, los callejones sin salida o los extremos de segmentos rotos. 6. Cuente los puntos restantes y divida por el área de estudio en km2.</span>"\
                "<br/><br/><b>Formula:</b><br/>"\
                "<span>Número de intersecciones / Superficie del área en Km2</span><br/>"