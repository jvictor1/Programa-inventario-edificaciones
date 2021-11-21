# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 09:57:20 2021

@author: Juan Camilo Victoria & Santiago Sepúlveda

    Este archivo funciona como ejemplo para correr las funciones que calculan
    la matriz de tipologías por municipio. Se puede leer más sobre cada función
    con CTR+I en spyder o ejecutando 'print(funcion.__doc__)'.
    Ejemplo: print(functions.func_principal.__doc__)
    
"""

import pros_taxonomy as tax
import utilities as ut

mapping_path = r'D:/Esquema_clasificacion_181021_3.xlsx' #ruta a archivo de mapping
result_path = r'D:\Universidad\[10]Décimo Semestre\Ingeniería Sísmica\Procesamiento datos del censo\GitHub\program/santander_ESTR.csv' #ruta a archivo con los resultados de número de edificaciones por combinación


# deptcod = ['68']
# deptname = ['Santander']


deptcod = ['05', '08', '11', '13', '15', '17', '18', '19', '20', '23', '25', '27', '41',
            '44', '47', '50', '52', '54', '63', '66', '68', '70', '73', '76', '81',
            '85', '86', '88', '91', '94', '95', '97', '99']

deptname = ['Antioquia', 'Atlantico', 'Bogota', 'Bolivar', 'Boyaca', 'Caldas', 'Caqueta',
            'Cauca', 'Cesar', 'Cordoba', 'Cundinamarca', 'Choco',
            'Huila', 'LaGuajira', 'Magdalena', 'Meta', 'Narino',
            'NorteDeSantander', 'Quindio', 'Risaralda', 'Santander',
            'Sucre', 'Tolima', 'ValleDelCauca', 'Arauca', 'Casanare',
            'Putumayo', 'SanAndresProvidenciaYSantaCatalina', 'Amazonas',
            'Guainia', 'Guaviare', 'Vaupes', 'Vichada']

exe_subdivi = False #True: se ejecuta a nivel manzana
#%% Ejecución cálculo de matriz de tipologías
exclude = [5001, 11001, 76001] #Se excluyen Medellín, Bogotá y Cali

conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2 = tax.read_input(mapping_path, result_path, mza=exe_subdivi)

tipologias, tiporesumen = tax.taxonomy(conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2, deptcod, exclude, mza=exe_subdivi)

#%% Agregar tipologías por # pisos

tipologias_agg = ut.aggregate(tipologias)

tipo_aggregate = ut.aggregate(tiporesumen)

#%% Save

# Matriz de tipologías por combinación de material
# ut.save_csv(tipologias, "output_TipologiasColombiaRural_disgregadas")
# Matriz de tipologías por municipio
# ut.save_csv(tiporesumen, "output_TipologiasColombiaRural_resumen")
# Matriz de tipologías agregada por # de pisos
# ut.save_csv(tipologias_agg, "output_TipologiasColombiaAggRural_disgregadas")
# ut.save_csv(tipo_aggregate, "output_TipologiasColombiaAggRural_resumen")