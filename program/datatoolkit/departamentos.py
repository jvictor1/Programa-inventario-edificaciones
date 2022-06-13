# -*- coding: utf-8 -*-
"""
    @author: Juan Camilo Victoria & Santiago Sepúlveda
    versión actualizada 13/06/2022
    
    Clase Departamentos
        Permite tener mejor organización
    
"""

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class Departamentos():
    
    #Class Variables
    
    _departments_codes = ['05', '08', '11', '13', '15', '17', '18', '19', '20', '23', '25', '27', '41',
                '44', '47', '50', '52', '54', '63', '66', '68', '70', '73', '76', '81',
                '85', '86', '88', '91', '94', '95', '97', '99']
    
    _departments_names = ['Antioquia', 'Atlantico', 'Bogota', 'Bolivar', 'Boyaca', 'Caldas', 'Caqueta',
                'Cauca', 'Cesar', 'Cordoba', 'Cundinamarca', 'Choco',
                'Huila', 'LaGuajira', 'Magdalena', 'Meta', 'Narino',
                'NorteDeSantander', 'Quindio', 'Risaralda', 'Santander',
                'Sucre', 'Tolima', 'ValleDelCauca', 'Arauca', 'Casanare',
                'Putumayo', 'SanAndresProvidenciaYSantaCatalina', 'Amazonas',
                'Guainia', 'Guaviare', 'Vaupes', 'Vichada']
    
    def __init__(self, departments_index):
        self.codes_analyse = [Departamentos._departments_codes[i] for i in departments_index]
        self.names_analyse = [Departamentos._departments_names[i] for i in departments_index]
        self.number_of_analyse = len(self.codes_analyse)
        
        return
