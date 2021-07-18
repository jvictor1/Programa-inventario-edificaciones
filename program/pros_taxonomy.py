# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:49:23 2020

@author: Juan Camilo Victoria & Santiago Sepúlveda
"""

import pandas as pd
import iteround
import numpy as np

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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

def read_input(mapping_path, result_path):
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
    mapping_ana = pd.ExcelFile(mapping_path)
    conteo_mpios = pd.read_csv(result_path)
    mpios_list = pd.read_csv(r'mpios_list.csv', encoding='ISO-8859-1')
    
    mapping_list = pd.read_excel(mapping_ana, sheet_name="mapping_list")
    mapping = pd.read_excel(mapping_ana, sheet_name="mapping")
    detailed_1 = pd.read_excel(mapping_ana, sheet_name="mapping_detailed_1", index_col=[0, 1]).reset_index()
    detailed_2 = pd.read_excel(mapping_ana, sheet_name="mapping_detailed_2", index_col=[0, 1]).reset_index()
    
    return conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2


def taxonomy(conteo_mpios, mpios_list, mapping_list, mapping, detailed_1, detailed_2, deptcod, exclude):
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
    tipologias = pd.DataFrame()
    tiporesumen = pd.DataFrame()
    for dptocod in deptcod:
        
        dptocod = int(dptocod)
        mpios_dpto = mpios_list[mpios_list["Departamento"] == dptocod]
            
        for mpiocod in mpios_dpto['COD']:
            
            mpios_filtered = mpios_dpto[mpios_dpto['COD'].isin([mpiocod])]
            
            if mpiocod in exclude:
                pass
            else:
                for m, data in mpios_filtered.iterrows():
                    mpio = int(data["COD"])
                    mpioname = data["Municipio_name"]
                    print("Iterando municipio:{}, {}".format(mpio, mpioname))
                    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    mpio_list = mapping_list[mapping_list["ID"] == mpio]
                    mpio_mapping = mpio_list["MAPPING"]
                    mpio_mapp1 = "_".join(mpio_mapping.tolist()[0].split("_")[:-1])
                    mpio_mapp2 = mpio_mapping.tolist()[0].split("_")[-1]
                    dist_mater = pd.DataFrame()

                    for i, row in mapping.iterrows():
                        
                        mat_pared = row["Material paredes/piso"]
                        flag = False
                        
                        for key, value in row.iloc[1:].iteritems():
                            
                            dist_dict = {}
                            
                            if (value == "detailed_1" or value == "detailed_2") and flag == False:

                                if value == "detailed_1":

                                    dist_comb = detailed_1[detailed_1["mapping"].str.contains(mpio_mapp1)]
                                    
                                else:

                                    dist_comb = detailed_2[detailed_2["mapping"].str.contains(mpio_mapp1)]
                                    
                                    
                                dist_comb = dist_comb[dist_comb["mapping"].str.contains(mpio_mapp2)]
                                    
                                cols = dist_comb.columns[2:]
                                for j, row in dist_comb.iterrows():
                                    
                                    viv_type = row["mapping"].split("_")[-1]
                                    
                                    for k in cols:
                                        
                                        porcentaje = row[k]
                                        dist_mater = dist_mater.append({"Material paredes": mat_pared, "Material piso": k, 
                                                           "Tipo de Vivienda": viv_type, "Combinación": row["Tipología"],
                                                           "Porcentaje": float(porcentaje/100)}, ignore_index=True)
                                flag = True
                                
                            else:
                                
                                dist_list = value.split()
                                
                                if len(dist_list) != 1:
                                    
                                    for p in range(0, len(dist_list), 2):

                                        dist_mater = dist_mater.append({"Material paredes": mat_pared, "Material piso": key, 
                                                           "Tipo de Vivienda": "No aplica", "Combinación": dist_list[p+1],
                                                           "Porcentaje": float(dist_list[p][:-1])/100}, ignore_index=True)
       
                    dist_mater_pivot = pd.pivot_table(dist_mater, index=['Material paredes', 'Material piso', 'Tipo de Vivienda'], columns=['Combinación'], values=['Porcentaje']).fillna(0).reset_index()   
                    dist_mater_pivot.columns = pd.Index(list(dist_mater_pivot.columns.get_level_values(0)[:3]) + list(dist_mater_pivot.columns.get_level_values(1)[3:]))
                    
                    dist_mater_pivot["Material paredes"] = dist_mater_pivot["Material paredes"].str.strip()
                    dist_mater_pivot["Material piso"] = dist_mater_pivot["Material piso"].str.strip()
                    dist_mater_pivot["Tipo de Vivienda"] = dist_mater_pivot["Tipo de Vivienda"].str.strip()
                    
                    conteo_estudio = conteo_mpios[conteo_mpios["COD"] == mpio]
                    
                    conteo_estudio.iloc[:]["Material Pared"] = conteo_estudio["Material Pared"].str.strip()
                    conteo_estudio.iloc[:]["Material Piso"] = conteo_estudio["Material Piso"].str.strip()
                    conteo_estudio.iloc[:]["Tipo Vivienda"] = conteo_estudio["Tipo Vivienda"].str.strip()
                    
                    for index, row in dist_mater_pivot.iterrows():
                        
                        if row["Tipo de Vivienda"] == "No aplica":
                            nedif_comb = conteo_estudio[(conteo_estudio["Material Pared"] == row["Material paredes"])\
                                    & (conteo_estudio["Material Piso"] == row["Material piso"])]["No. edificaciones"].sum()
                        else:
                            nedif_comb = conteo_estudio[(conteo_estudio["Material Pared"] == row["Material paredes"])\
                                    & (conteo_estudio["Material Piso"] == row["Material piso"]) \
                                    & (conteo_estudio["Tipo Vivienda"] == row["Tipo de Vivienda"])]["No. edificaciones"]
                        
                            nedif_comb = nedif_comb.to_list()
                            if not nedif_comb:
                                nedif_comb = 0
                                
                        dist_mater_pivot.iloc[index, 3:] = dist_mater_pivot.iloc[index, 3:] * nedif_comb
                            
                    
                    for i in range(len(dist_mater_pivot)):
                        dist_mater_pivot.iloc[i, 3:] = round_series_retain_integer_sum(dist_mater_pivot.iloc[i, 3:])
                    
                    dist_mater_pivot = dist_mater_pivot.assign(cod = mpio)
                    dist_mater_pivot = dist_mater_pivot.assign(mpio_name = mpioname)
                    
                    dist_mater_res = dist_mater_pivot.drop(columns=["Material paredes", 
                                                                    "Material piso", 
                                                                    "Tipo de Vivienda"])
                    
                    dist_mater_res = dist_mater_res.groupby(["cod", "mpio_name"]).sum().reset_index()
                    
                    tipologias = tipologias.append(dist_mater_pivot, ignore_index=True)
                    tiporesumen = tiporesumen.append(dist_mater_res, ignore_index=True)
                    
                    
                    print("Terminado municipio:{}, {}".format(mpio, mpioname))
            
                    tipologias = tipologias.fillna(0)
                    tiporesumen = tiporesumen.fillna(0)
                    
    return tipologias, tiporesumen