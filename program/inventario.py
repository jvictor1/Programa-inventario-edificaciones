# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 09:51:55 2021

@author: Juan Camilo Victoria & Santiago Sepúlveda

    Este archivo funciona como ejemplo para ejecutar las funciones que procesan
    los datos del DANE para obtener un inventario detallado de las edificaciones
    de un municipio o departamento. Se puede leer más sobre cada función con
    CTR+I en spyder o ejecutando 'print(funcion.__doc__)'.
    Ejemplo: print(functions.func_principal.__doc__)
    
"""

import procesamiento_datos as functions
import utilities as ut

ruta_carpetas = r'D:\Universidad\[10]Décimo Semestre\Ingeniería Sísmica\Procesamiento datos del censo\Departamentos'     # ruta con las carpetas de las bases de datos


# deptcod = ['68']
# deptname = ['Santander']

deptcod = ['91']
deptname = ['Amazonas']


# deptcod = ['05', '08', '11', '13', '15', '17', '18', '19', '20', '23', '25', '27', '41',
#             '44', '47', '50', '52', '54', '63', '66', '68', '70', '73', '76', '81',
#             '85', '86', '88', '91', '94', '95', '97', '99']

# deptname = ['Antioquia', 'Atlantico', 'Bogota', 'Bolivar', 'Boyaca', 'Caldas', 'Caqueta',
#             'Cauca', 'Cesar', 'Cordoba', 'Cundinamarca', 'Choco',
#             'Huila', 'LaGuajira', 'Magdalena', 'Meta', 'Narino',
#             'NorteDeSantander', 'Quindio', 'Risaralda', 'Santander',
#             'Sucre', 'Tolima', 'ValleDelCauca', 'Arauca', 'Casanare',
#             'Putumayo', 'SanAndresProvidenciaYSantaCatalina', 'Amazonas',
#             'Guainia', 'Guaviare', 'Vaupes', 'Vichada']

#%% Opciones de filtrado

filtClase=[1, 2]
filtUnidad=[1, 2]
filtViv=[1, 2, 3]

exe_manzana = False
exe_resumen = False

#%% Ejecución Ejemplo Pre procesamiento de archivos del DANE
result_dptos, resumen_dptos, resumen_mpios, result_nedifstr, result_mode, result_nedif = functions.func_principal(ruta_carpetas, deptcod, deptname, filtClase, filtUnidad, filtViv, exe_manzana, exe_resumen)

#%% Save
# Result dptos archivo base para calcular la matriz de tipologías
# ut.save_csv(result_dptos, "output_resultcombinacionColombia")
# Resumen dptos dataframe con el resumen de conteo por municipio
# ut.save_csv(resumen_dptos, "output_resumenconteo")
# Resumen mpios dataframe con el resumen de conteo por manazana y municipio
# ut.save_csv(resumen_mpios, "output_resumenconteoManzana")
