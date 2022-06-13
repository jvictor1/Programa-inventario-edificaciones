# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 09:51:55 2021

    @author: Juan Camilo Victoria & Santiago Sepúlveda
    versión actualizada 13/06/2022

    Este archivo funciona como ejemplo para ejecutar las funciones que procesan
    los datos del DANE para obtener un inventario detallado de las edificaciones
    de un municipio o departamento. Se puede leer más sobre cada función con
    CTR+I en spyder o ejecutando 'print(funcion.__doc__)'.
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

from datatoolkit import ProcessTheData

#%% Ejemplo del uso de la clase ProcessTheData

folder_path = r'/Users/juancamilo/Proyectos/'     # ruta con las carpetas de las bases de datos por ejemplo 99Vichada

#%% Input Options

filtClase=[1, 2]
filtUnidad=[1, 2]
filtViv=[1, 2, 3]

departments_index = [32]

group_by_ages = False
do_resumen = False

filters = (filtClase, filtUnidad, filtViv)
extra_options = (group_by_ages, do_resumen)

#%% Ejecución Se inicializa un objeto de clase ProcessTheData
### El objeto contiene todas las variable utilizadas y también los resultados
### Se puede acceder a las variables deseadas con el path objeto.variable
myInventario = ProcessTheData(folder_path, departments_index, filters, extra_options)

### Acceso al resultado de edificaciones en formato string
resultado_nedifstr = myInventario.df_merged_nedifstr

#%% Guardar los archivos de salida opcional método save_results
myInventario.save_results(save_path='')



