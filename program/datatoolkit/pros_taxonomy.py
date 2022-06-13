# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:49:23 2020

    @author: Juan Camilo Victoria & Santiago Sepúlveda
    versión actualizada 13/06/2022
    
    Módulo que tiene como función principal el tratamiento de los datos de inventario
    junto con un esquema de clasificación para generar una taxonomía.
    
    Para esto, la clase Taxonomy contiene los métodos necesarios para
    leer, procesar y escribir.
    
    Taxonomy: Permite crear una instancia para el procesamiento de un esquema de clasificación
                y un inventario de edificaciones
    
    Los argumentos de entrada:
        
        mapping_path: Ruta al archivo que contiene el esquema.
        inventory_path: Ruta al archivo que contiene el inventario de edificaciones.
        departments_index: Índice que corresponde a los departamentso que se desean analizar
                            Lista de enteros (0-32).
        exclude_list: Lista de enteros que corresponde a los códigos de municipios que se deseeen excluir.
        do_manzana: Boolean que permite ejecutar o no taxonomía a nivel de manazana 
                        (True/False)
                
"""

import pandas as pd
import numpy as np
import time
import os
import datatoolkit.utilities as ut
from datatoolkit.departamentos import Departamentos


#%% Clase Taxonomy -> mapping scheme
class Taxonomy(Departamentos):
    
    def __init__(self, mapping_path, inventory_path, departments_index, exclude_list=[], do_manzana = False):
        self.mapping_path = mapping_path
        self.inventory_path = inventory_path
        self.exclude_list = exclude_list
        self.do_manzana = do_manzana
        
        Departamentos.__init__(self, departments_index)
        
        #Ejecución de funciones principales
        conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2 = self._read_input()
        self.main(conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2)
        
        
    @staticmethod
    def round_series_retain_integer_sum(xs):
        """
        Function to round a list of decimal values and mantain the sum
    
        Parameters
        ----------
        xs : list
            List of decimal values.
    
        Returns
        -------
        ys : list
            List of integers.
    
        """
        N = sum(xs)
        Rs = [int(x) for x in xs]
        K = N - sum(Rs)
        # print(K, round(K))
        assert round(K) == round(K)
        fs = [x - int(x) for x in xs]
        indices = [i for order, (e, i) in enumerate(reversed(sorted((e,i) for i,e in enumerate(fs)))) if order < round(K)]
        ys = [R + 1 if i in indices else R for i,R in enumerate(Rs)]
        
        return ys
    
    def aggregate_tipologias(self):
        return ut.aggregate(self.df_tipologias)
    
    def aggregate_tipologias_resumen(self):
        return ut.aggregate(self.df_tipologias_resumen)
    
    def save_results(self, save_path=''):
        """
        Save the result (df_tipologias, df_tipologias_resumen) DataFrames in csv format and store the path

        Parameters
        ----------
        save_path : optional 
            path to desired save folder.
        Returns
        -------
        None.

        """
        self.df_tipologias.to_csv(save_path + "df_tipologias.csv", index=False)
        self.df_tipologias_resumen.to_csv(save_path + "df_tipologias_resumen.csv", index=False)
        
        return
        
    
    def _read_input(self):
        """
        
    
        Parameters
        ----------
        mapping_path : string (path)
            Absolute or relative path to the mapping xlsx file.
        result_path : string (path)
            Absolute or relative path to the csv file with results of MAT distribution.
    
        Returns
        -------
        conteo_mpios : pandas DataFrame
            DESCRIPTION.
        mpios_list : pandas DataFrame
            DESCRIPTION.
        mapping_list : pandas DataFrame
            DESCRIPTION.
        mapping : pandas DataFrame
            DESCRIPTION.
        detailed_1 : pandas DataFrame
            DESCRIPTION.
        detailed_2 : pandas DataFrame
            DESCRIPTION.
    
        """
        mapping_ana = pd.ExcelFile(self.mapping_path)
        conteo_mpios = pd.read_csv(self.inventory_path)
        mpios_list = pd.read_csv(os.path.dirname(ut.__file__) + '/mpios_list.csv', encoding='ISO-8859-1')
        
        mapping_list = pd.read_excel(mapping_ana, sheet_name="mapping_list")
        mapping = pd.read_excel(mapping_ana, sheet_name="mapping")
        detailed_1 = pd.read_excel(mapping_ana, sheet_name="mapping_detailed_1", index_col=[0, 1]).reset_index()
        detailed_2 = pd.read_excel(mapping_ana, sheet_name="mapping_detailed_2", index_col=[0, 1]).reset_index()
        
        return conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2
    
    
    def main(self, conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2):
        """
        Principal function. Calculate the taxonomy distribution based on mapping and MAT distribution.
        Returns two main dataframes which one contains taxonomy matrix grouped by municipality and 
        other, taxonomy by municipality and MAT combination.
    
        Parameters
        ----------
        conteo_mpios : pandas DataFrame
            Input data with the results of the MAT distribution.
        mpios_list : pandas DataFrame
            List of municipalities considered by DANE.
        mapping_list : pandas DataFrame
            Input.
        mapping : pandas DataFrame
            Input.
        detailed_1 : pandas DataFrame
            Input.
        detailed_2 : pandas DataFrame
            Input.
        deptcod : list
            List containing one or more department code.
        exclude : list
            List with municipalitites to be excluded.
    
        Returns
        -------
        tipologias : pandas DataFrame
            Contains the number of buildings by typology and MAT combination for each municipality.
        tiporesumen : list
            Contains the number of buildings by typology for each municipality.
    
        """
        start = time.time()
        
        tipologias = pd.DataFrame()
        tiporesumen = pd.DataFrame()
        for dptocod in self.codes_analyse:
            
            dptocod = int(dptocod)
            mpios_dpto = mpios_list[mpios_list["Departamento"] == dptocod]
                
            for mpiocod in mpios_dpto['COD']:
                
                mpios_filtered = mpios_dpto[mpios_dpto['COD'].isin([mpiocod])]
                
                ##Revisa la lista de exclusiones
                if mpiocod in self.exclude_list:
                    pass
                else:
                    #Iteración por municipio
                    for m, data in mpios_filtered.iterrows():
                        mpio = int(data["COD"])
                        mpioname = data["Municipio_name"]
                        print("Iterando municipio:{}, {}".format(mpio, mpioname))
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        mpio_list = mapping_list[mapping_list["ID"] == mpio]
                        mpio_mapping = mpio_list["MAPPING"]
                        mpio_mapp = mpio_mapping.tolist()[0]
                        dist_mater = pd.DataFrame()
    
                        for i, row in mapping.iterrows():
                            
                            mat_pared = row["Material paredes/piso"]
                            
                            for key, value in row.iloc[1:].iteritems():
                            
                                if (value == "detailed_1" or value == "detailed_2"):
                                    
                                    if value == "detailed_1":
                                        
                                        dist_comb = detailed_1[detailed_1["mapping"].str.contains(mpio_mapp, regex=False)]
                                    else:
                                        dist_comb = detailed_2[detailed_2["mapping"].str.contains(mpio_mapp, regex=False)]
                                    
                                    
                                    for j, row in dist_comb.iterrows():
                                        
                                        viv_type = row["mapping"].split("_")[-1]
                                        
                                        if viv_type not in ["Apartamento", "Casa"]:
                                            viv_type = "No aplica"
                                        
                                        porcentaje = row[key]
                                        
                                        dist_mater = dist_mater.append({"Material Pared": mat_pared, "Material Piso": key, 
                                                           "Tipo Vivienda": viv_type, "Combinación": row["Tipología"],
                                                           "Porcentaje": float(porcentaje/100)}, ignore_index=True)
                                    
                                else:
                                    
                                    dist_list = value.split()
                                    
                                    if len(dist_list) != 1:
                                        
                                        for p in range(0, len(dist_list), 2):
                                            
                                            dist_mater = dist_mater.append({"Material Pared": mat_pared, "Material Piso": key, 
                                                               "Tipo Vivienda": "No aplica", "Combinación": dist_list[p+1],
                                                               "Porcentaje": float(dist_list[p][:-1])/100}, ignore_index=True)
           
                        dist_mater_pivot = pd.pivot_table(dist_mater, index=['Material Pared', 'Material Piso', 'Tipo Vivienda'], columns=['Combinación'], values=['Porcentaje'], aggfunc=np.sum).fillna(0).reset_index()   
                        dist_mater_pivot.columns = pd.Index(list(dist_mater_pivot.columns.get_level_values(0)[:3]) + list(dist_mater_pivot.columns.get_level_values(1)[3:]))
                        
                        dist_mater_pivot["Material Pared"] = dist_mater_pivot["Material Pared"].str.strip()
                        dist_mater_pivot["Material Piso"] = dist_mater_pivot["Material Piso"].str.strip()
                        dist_mater_pivot["Tipo Vivienda"] = dist_mater_pivot["Tipo Vivienda"].str.strip()
                        
                        conteo_estudio = conteo_mpios[conteo_mpios["cod"] == mpio]
                        
                        conteo_estudio.iloc[:]["Material Pared"] = conteo_estudio["Material Pared"].str.strip()
                        conteo_estudio.iloc[:]["Material Piso"] = conteo_estudio["Material Piso"].str.strip()
                        conteo_estudio.iloc[:]["Tipo Vivienda"] = conteo_estudio["Tipo Vivienda"].str.strip()
                        
                        if self.do_manzana:
                            subdivi = conteo_estudio[["cod", "Municipio", "UA_CLASE", "U_SECT_RUR", 
                                                "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", 
                                                "U_SECC_URB", "U_MZA"]].copy()
                            subdivi = subdivi.drop_duplicates()
                            
                            dist_mater_mza = pd.DataFrame()
                            for i, j in subdivi.iterrows():
                                dist_mater_pmza = dist_mater_pivot.copy()
                                
                                jframe = j.to_frame().T
                                conteo_mza = conteo_estudio.merge(jframe, on=["cod", "Municipio", "UA_CLASE", "U_SECT_RUR", 
                                                                "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", 
                                                                "U_SECC_URB", "U_MZA"])
                                                                                              
                                for index, row in dist_mater_pivot.iterrows():
                                    if row["Tipo Vivienda"] == "No aplica":
                                        is_in = conteo_mza.isin([row["Material Pared"], row["Material Piso"], row["Tipo Vivienda"]])
                                        if is_in["Material Pared"].any() == True and is_in["Material Piso"].any() == True and is_in["Tipo Vivienda"].all() == False:
                                            
                                            cidx= conteo_mza.index[(conteo_mza["Material Pared"] == row["Material Pared"]) & 
                                                   (conteo_mza["Material Piso"] == row["Material Piso"])].tolist()
                                            conteo_mza.loc[cidx, "Tipo Vivienda"] = "No aplica"
                                        
                                        nedif_comb = conteo_mza[(conteo_mza["Material Pared"] == row["Material Pared"])\
                                                & (conteo_mza["Material Piso"] == row["Material Piso"])]["No. edificaciones"].sum()
                                    else:
                                        nedif_comb = conteo_mza[(conteo_mza["Material Pared"] == row["Material Pared"])\
                                                & (conteo_mza["Material Piso"] == row["Material Piso"]) \
                                                & (conteo_mza["Tipo Vivienda"] == row["Tipo Vivienda"])]["No. edificaciones"]
                                    
                                        nedif_comb = nedif_comb.to_list()
                                        if not nedif_comb:
                                            nedif_comb = 0
                                        else:
                                            nedif_comb = sum(nedif_comb)
                                            
                                    dist_mater_pmza.iloc[index, 3:] = dist_mater_pmza.iloc[index, 3:] * nedif_comb
                                
                                conteo_mza = conteo_mza.groupby(["Municipio", "UA_CLASE", "U_SECT_RUR", 
                                                                "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", 
                                                                "U_SECC_URB", "U_MZA", 'Material Pared','Material Piso', 'Tipo Vivienda'])[['No. edificaciones',
                                          'TPER', 'THOG', 'THOM', 'TMUJ', 
                                          'T00', 'T05', 'T10', 'T15', 'T20', 
                                          'T25', 'T30', 'T35', 'T40', 'T45', 
                                          'T50', 'T55', 'T60', 'T65', 'T70', 
                                          'T75', 'T80', 'T85', 'T90', 'T95', 'T100']].sum().reset_index()
                                
                                dist_mater_merge = conteo_mza.merge(dist_mater_pmza,on=['Material Pared','Material Piso', 'Tipo Vivienda'])
                                
                                dist_mater_mza = dist_mater_mza.append(dist_mater_merge, ignore_index=True)
                            
                            dist_mater_pivot = dist_mater_mza        
                            
                        else:
                            
                            for index, row in dist_mater_pivot.iterrows():
                                
                                if row["Tipo Vivienda"] == "No aplica":
                                    nedif_comb = conteo_estudio[(conteo_estudio["Material Pared"] == row["Material Pared"])\
                                            & (conteo_estudio["Material Piso"] == row["Material Piso"])]["No. edificaciones"].sum()
                                else:
                                    nedif_comb = conteo_estudio[(conteo_estudio["Material Pared"] == row["Material Pared"])\
                                            & (conteo_estudio["Material Piso"] == row["Material Piso"]) \
                                            & (conteo_estudio["Tipo Vivienda"] == row["Tipo Vivienda"])]["No. edificaciones"]
                                
                                    nedif_comb = nedif_comb.to_list()
                                    if not nedif_comb:
                                        nedif_comb = 0
                                    else:
                                        nedif_comb = sum(nedif_comb)
                                        
                                dist_mater_pivot.iloc[index, 3:] = dist_mater_pivot.iloc[index, 3:] * nedif_comb
                                
                                       
                        dist_mater_pivot.insert(0, 'cod', mpio)
                        dist_mater_pivot.insert(1, 'mpio_name', mpioname)
                        
                        dist_mater_res = dist_mater_pivot.drop(columns=["Material Pared", 
                                                                        "Material Piso", 
                                                                        "Tipo Vivienda"])
                        
                        if self.do_manzana:
                            dist_mater_res = dist_mater_res.groupby(["cod", "mpio_name", "Municipio", "UA_CLASE", "U_SECT_RUR", 
                                                                "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", 
                                                                "U_SECC_URB", "U_MZA"]).sum().reset_index()
                        else:
                            dist_mater_res = dist_mater_res.groupby(["cod", "mpio_name"]).sum().reset_index()
                        
                        tipologias = tipologias.append(dist_mater_pivot, ignore_index=True)
                        tiporesumen = tiporesumen.append(dist_mater_res, ignore_index=True)
                        
                        
                        print("Terminado municipio:{}, {}".format(mpio, mpioname))
                
                        tipologias = tipologias.fillna(0)
                        tiporesumen = tiporesumen.fillna(0)
        
        
        idx = tipologias.columns.get_loc('ADO|EU/LWAL+DNO/H:1')
        tipologias.iloc[:, idx:] = tipologias.iloc[:, idx:].apply(Taxonomy.round_series_retain_integer_sum, axis=1).to_list()
        idx = tiporesumen.columns.get_loc('ADO|EU/LWAL+DNO/H:1')
        tiporesumen.iloc[:, idx:] = tiporesumen.iloc[:, idx:].apply(Taxonomy.round_series_retain_integer_sum, axis=1).to_list()
    
        self.df_tipologias = tipologias
        self.df_tipologias_resumen = tiporesumen
        
        end = time.time()
        print('Elapsed time: {} s'.format(end-start))
    
        return

