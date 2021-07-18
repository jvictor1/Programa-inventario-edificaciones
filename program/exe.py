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

mpios_list = r'D:\Universidad\[10]Décimo Semestre\Ingeniería Sísmica\Procesamiento datos del censo/mpios_list.csv'         # ruta a lista mpios con codigos y nombre depto
ruta_carpetas = r'D:\Universidad\[10]Décimo Semestre\Ingeniería Sísmica\Procesamiento datos del censo\Departamentos'     # ruta con las carpetas de las bases de datos
##
mapping_path = r'D:\Universidad\[10]Décimo Semestre\Ingeniería Sísmica\Procesamiento datos del censo\Mapping/Mapping_ANA_220321_modificado.xlsx' #ruta a archivo de mapping
result_path = r'D:\Universidad\[10]Décimo Semestre\Ingeniería Sísmica\Procesamiento datos del censo/resultado_comb_mpios_completo.csv' #ruta a archivo con los resultados de número de edificaciones por combinación

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

#%% Ejecución Ejemplo Pre procesamiento de archivos del DANE
# result_dptos, resumen_dptos, resumen_mpios, result_nedifstr, result_mode, result_nedif = functions.func_principal(ruta_carpetas, deptcod, deptname, [1, 2], [1, 2], [1, 2, 3], False, True)

#%% Ejecución cálculo de matriz de tipologías
exclude = [5001, 11001, 76001] #Se excluyen Medellín, Cali y Bogotá

conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2 = tax.read_input(mapping_path, result_path)

tipologias, tiporesumen = tax.taxonomy(conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2, deptcod, exclude)

#%% Agregar tipologías por # pisos

tipo_aggregate = ut.aggregate(tiporesumen)

#%% Save
# Result dptos archivo base para calcular la matriz de tipologías
# ut.save_csv(result_dptos, "output_resultcombinacion")
# Resumen dptos dataframe con el resumen de conteo por municipio
# ut.save_csv(resumen_dptos, "output_resumenconteo")
# Resumen mpios dataframe con el resumen de conteo por manazana y municipio
# ut.save_csv(resumen_mpios, "output_resumenconteoManzana")
# Matriz de tipologías por combinación de material
# ut.save_csv(tipologias, "Tipologias_disgregadas")
# Matriz de tipologías por municipio
# ut.save_csv(tiporesumen, "Tipologias_Mpios.csv")
# Matriz de tipologías agregada por # de pisos
# ut.save_csv(tipo_aggregate, "TipologiasAgg_Mpios.csv")
