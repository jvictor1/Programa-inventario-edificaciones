# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 21:01:23 2021

@author: Juan Camilo Victoria & Santiago Sepúlveda

    Este archivo funciona como ejemplo para correr las funciones que procesan
    los datos del DANE y también las funciones que calculan la matriz de tipologías
    por municipio. Se puede leer más sobre cada función con CTR+I en spyder
    o ejecutando 'print(funcion.__doc__)'.
    Ejemplo: print(functions.func_principal.__doc__)
    
"""

import procesamiento_datos as functions
import pros_taxonomy as tax
import utilities as ut

mpios_list = r'D:\Eafit\ModeloExposicion\Scripts\Codigos para github\Programa-inventario-edificaciones-main\program'         # ruta a lista mpios con codigos y nombre depto
ruta_carpetas = r'D:\Eafit\ModeloExposicion\BasesDeDatos'     # ruta con las carpetas de las bases de datos
##
mapping_path = r'D:\Eafit\ModeloExposicion\Scripts\Codigos para github\Programa-inventario-edificaciones-main\files' #ruta a archivo de mapping
result_path = r'D:\Eafit\ModeloExposicion\Scripts\Codigos para github\Programa-inventario-edificaciones-main' #ruta a archivo con los resultados de número de edificaciones por combinación

deptcod = ['94', '99']
deptname = ['Guainia', 'Vichada']

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

#%% Ejecución Ejemplo inventario edificios y personas resumen por municipio
result_dptos, resumen_dptos, resumen_mpios, result_nedifstr, result_mode, result_nedif = functions.func_principal(ruta_carpetas, deptcod, deptname, [1, 2], [1, 2], [1, 2, 3], True, True)

#%% Ejecución Ejemplo inventario edificios y personas detallado por manzana
result_dptos, resumen_dptos, resumen_mpios, result_nedifstr, result_mode, result_nedif = functions.func_principal(ruta_carpetas, deptcod, deptname, [1, 2], [1, 2], [1, 2, 3], True, True)
