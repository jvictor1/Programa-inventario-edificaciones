# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 09:57:20 2021

@author: Juan Camilo Victoria & Santiago Sepúlveda
versión actualizada 13/06/2022

    Este archivo funciona como ejemplo para correr las funciones que calculan
    la matriz de tipologías por municipio. Se puede leer más sobre cada función
    con CTR+I en spyder o ejecutando 'print(funcion.__doc__)'.
    Ejemplo: print(functions.func_principal.__doc__)
    
    La lista de departamentos a considerar debe ingresarse a manera de índices (0-32)
    cada índice corresponde a un departamento en la lista de departamentos organizados
    incrementalmente segun el código de departamento. Es decir, Antioquia es 0, Vichada 32.
    
    Codigos = ['05', '08', '11', '13', '15', '17', '18', '19', '20', '23', '25', '27', '41',
                '44', '47', '50', '52', '54', '63', '66', '68', '70', '73', '76', '81',
                '85', '86', '88', '91', '94', '95', '97', '99']
    
    Nombres = ['Antioquia', 'Atlantico', 'Bogota', 'Bolivar', 'Boyaca', 'Caldas', 'Caqueta',
                'Cauca', 'Cesar', 'Cordoba', 'Cundinamarca', 'Choco',
                'Huila', 'LaGuajira', 'Magdalena', 'Meta', 'Narino',
                'NorteDeSantander', 'Quindio', 'Risaralda', 'Santander',
                'Sucre', 'Tolima', 'ValleDelCauca', 'Arauca', 'Casanare',
                'Putumayo', 'SanAndresProvidenciaYSantaCatalina', 'Amazonas',
                'Guainia', 'Guaviare', 'Vaupes', 'Vichada']
    
    Index = [0, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30, 31, 32]

    
    
"""

from datatoolkit import Taxonomy

#%% Opcional -> Ejemplo del uso de la clase Taxonomy

mapping_path = r'../files/Mapping_Template.xlsx' #ruta a archivo de mapping
inventory_path = r'../results/Inventario_Colombia_Urbano_171121.csv' #ruta a archivo con los resultados de número de edificaciones por combinación


#%% Input options
departments_index = [32]
do_subdivicion_manzana = False #True: se ejecuta a nivel manzana
exclude_list = [5001, 11001, 76001] #Se excluyen Medellín, Bogotá y Cali

#%% Inicialización de instancia de tipo Taxonomy
### Los dos últimos argumentos son opcionales (lista de exclusión y opcional de ejectuar la taxonomía a nivel de manzana)
myTaxonomy = Taxonomy(mapping_path, inventory_path, departments_index, exclude_list, do_subdivicion_manzana)

### El acceso a las variables de la instancia se hacen con el formato
### objeto.variable
### Los principales resultados son df_tipologias, df_tipologias_resumen
df_tipologias = myTaxonomy.df_tipologias

### Opcional la instancia tiene un método 'aggregate_tipologias' y 'aggregate_tipologias_resumen' que permite realizar un agregado por # de pisos
df_agg_tipologias = myTaxonomy.aggregate_tipologias()

#%% Guardar los archivos de salida opcional método save_results
myTaxonomy.save_results(save_path='')