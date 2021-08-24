# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 09:30:17 2020

@author: Juan Camilo Victoria & Santiago Sepúlveda
"""

from __future__ import division
import numpy as np
import pandas as pd
import time
from functools import reduce

#%% Funciones
def cambio_variable(var, idx):
    """
    Changes numerical value for string values according to variable dictionary from DANE

    Parameters
    ----------
    var : str
        String identifying variable.
    idx : int
        Numerical value obtained from (VIV, PER) data from DANE.

    Returns
    -------
    str
        Returns the corresponding string value from specified variable.

    """
    TVIV = {0: 'Sin información',
            1: 'Casa',
            2: 'Apartamento',
            3: 'Tipo Cuarto'}
    
    MPARED = {0: 'Sin información',
              1: 'Bloque, ladrillo, piedra, madera pulida',
              2: 'Concreto vaciado',
              3: 'Material prefabricado',
              4: 'Guadua',
              5: 'Tapia pisada, bahareque, adobe',
              6: 'Madera burda, tabla, tablón',
              7: 'Caña, esterilla, otros vegetales',
              8: 'Madera burda, tabla, tablón, otro vegetal',
              9: 'No tiene paredes'}
    
    MPISO = {0: 'Sin información',
             1: 'Mármol, parqué, madera pulida y lacada',
             2: 'Baldosa, vinilo, tableta, ladrillo, laminado',
             3: 'Alfombra',
             4: 'Cemento, gravilla',
             5: 'Madera burda, tabla, tablón, otro vegetal',
             6: 'Tierra, arena, barro'}

    
    if var == 'V_TIPO_VIV_VS1':
        
        return TVIV[idx]
    
    elif var == 'V_MAT_PARED_VS1':
        
        return MPARED[idx]
    
    elif var == 'V_MAT_PISO_VS1':
        
        return MPISO[idx]
    
def func_mode(x):
    """
    Calculates a conditional mode for the MAT variables

    Parameters
    ----------
    x : list
        List that contains MAT values.

    Returns
    -------
    int
        Returns the conditioned integer mode.

    """    
    if len(pd.Series.mode(x)) > 1 and pd.Series.mode(x)[0] == 0:
        
        return pd.Series.mode(x)[1]
    
    else:
        
        if pd.Series.mode(x)[0] != 0:
            
            return pd.Series.mode(x)[0]
        
        elif len(pd.Series.value_counts(x)) > 1 and pd.Series.value_counts(x).index[0] == 0:
            
            return pd.Series.value_counts(x).index[1]
        
        else:
            
            return pd.Series.value_counts(x).index[0]

def func_mode_tviv(x):
    """
    Calculates a conditional mode for the Type VIV variables
    changing type 3 viv for 1 or 2

    Parameters
    ----------
    x : list
        List that contains TVIV values.

    Returns
    -------
    int
        Returns the conditioned integer mode.

    """    
    if len(pd.Series.mode(x)) > 1 and pd.Series.mode(x)[0] == 3:
        
        return pd.Series.mode(x)[1]
    
    else:
        
        if pd.Series.mode(x)[0] != 3:
            
            return pd.Series.mode(x)[0]
        
        elif len(pd.Series.value_counts(x)) > 1 and pd.Series.value_counts(x).index[0] == 3:
            
            return pd.Series.value_counts(x).index[1]
        
        else:
            
            return np.random.randint(1, high=3)
        
def read_files(folder_path, dptocod, depto):
    """
    Read the MGN, VIV, PER files and list containing 1122 Colombian municipalities from the specified folder path

    Parameters
    ----------
    folder_path : string (absolute or relative path)
        DESCRIPTION.
    dptocod : int
        Code of the department to import files.
    depto : int
        Name of the department to import files.

    Returns
    -------
    mgn : pandas DataFrame
        MGN data.
    viv : pandas DataFrame
        VIV data.
    per : pandas DataFrame
        per data.
    mpios_list : pandas DataFrame
        list containing 1122 Colombian municipalities considered by DANE.

    """
    filepath = folder_path + '/{}/'.format(str(dptocod) + depto)
    f_mgn = r"CNPV2018_MGN_A2_{}.CSV".format(dptocod)
    f_viv = r"CNPV2018_1VIV_A2_{}.CSV".format(dptocod)
    f_per = r"CNPV2018_5PER_A2_{}.CSV".format(dptocod)
        
    mgn = pd.read_csv(filepath + f_mgn)
    viv = pd.read_csv(filepath + f_viv)
    per = pd.read_csv(filepath + f_per)   
    
    mpios_list = pd.read_csv("mpios_list.csv", encoding="ISO-8859-1")
    
    return mgn, viv, per, mpios_list


def filter_files(mgn, viv, per, filtClase=None, filtUnidad=[1, 2], filtViv=[1, 2, 3]):
    """
    Filter DataFrames by Uso Unidad, Tipo Vivienda

    Parameters
    ----------
    mgn : pandas DataFrame
        DESCRIPTION.
    viv : pandas DataFrame
        DESCRIPTION.
    per : pandas DataFrame
        DESCRIPTION.
    filtClase : list, optional
        List containing the numerical values of Clase to be filtered. The default is None.
    filtUnidad : list, optional
        List containing the numerical values of USO_UNIDAD to be filtered. The default is [1, 2].
    filtViv : list, optional
        List containing the numerical values of TIPO_VIVIENDA to be filtered. The default is [1, 2, 3].

    Returns
    -------
    mgn : pandas DataFrame
        Filtered pandas DataFrame.
    viv : pandas DataFrame
        Filtered pandas DataFrame.
    per : pandas DataFrame
        Filtered pandas DataFrame.

    """
    # Fill NaN values with other values
    viv['V_MAT_PARED'] = viv['V_MAT_PARED'].fillna(0)
    viv['V_MAT_PISO'] = viv['V_MAT_PISO'].fillna(0)
    viv['VA1_ESTRATO'] = viv['VA1_ESTRATO'].fillna(10)
    per["P_NROHOG"] = per["P_NROHOG"].fillna(1)
    
    try:
        "An error will occur if the filter input parameter is different from a list"
        
        ## Cabecera Municipal clase = 1 Centro Poblado clase = 2
        #Filter MGN, VIV, PER data by CLASE
        if filtClase:
            
            mgn = mgn[mgn["UA_CLASE"].isin(filtClase)]
            viv = viv[viv["UA_CLASE"].isin(filtClase)]
            per = per[per["UA_CLASE"].isin(filtClase)]
        
        #Filter VIV data by USO_UNIDAD and TIPO_VIV
        viv = viv[viv['UVA_USO_UNIDAD'].isin(filtUnidad)] #Uso vivienda y uso mixto
        viv = viv[viv['V_TIPO_VIV'].isin(filtViv)]  #Tipo vivienda Casa Apartamento Cuarto
    except:
        pass    
    
    return mgn, viv, per


def organize_personas(perestudio):
    """
    Stack original PERSONAS data by COD_ENCUESTAS in order to get a DataFrame with same format as
    VIV and MGN data.

    Parameters
    ----------
    perestudio : pandas DataFrame
        Personas DataFrame without modifications.

    Returns
    -------
    personas : pandas DataFrame
        Personas DataFrame grouped by COD_ENCUESTAS.

    """
    dicedad = {1: 'T00', 2:'T05', 3:'T10', 4:'T15', 5:'T20', 6:'T25', 7:'T30', 8:'T35', 
               9:'T40', 10:'T45', 11:'T50', 12:'T55', 13:'T60', 14:'T65', 15:'T70', 16:'T75', 
               17:'T80', 18:'T85', 19:'T90', 20:'T95', 21:'T100'}
    
    dicgen = {1: 'THOM', 2: 'TMUJ'}
    
    permpio = pd.DataFrame(columns = ['COD_ENCUESTAS',
                                  'THOG', 'TPER', 'THOM', 'TMUJ', 
                                  'T00', 'T05', 'T10', 'T15', 'T20', 
                                  'T25', 'T30', 'T35', 'T40', 'T45', 
                                  'T50', 'T55', 'T60', 'T65', 'T70', 
                                  'T75', 'T80', 'T85', 'T90', 'T95', 'T100'])
    
    pdnro = perestudio.groupby(["COD_ENCUESTAS"])[["P_NROHOG", "P_NRO_PER"]].nunique().reset_index()
    psexo = perestudio.groupby(["COD_ENCUESTAS", "P_SEXO"]).size().unstack(fill_value=0).reset_index()
    pedad = perestudio.groupby(["COD_ENCUESTAS", "P_EDADR"]).size().unstack(fill_value=0).reset_index()
    
    pdnro.rename(columns = {"P_NROHOG": "THOG", "P_NRO_PER": "TPER"}, inplace=True)
    psexo.rename(columns = dicgen, inplace=True)
    pedad.rename(columns = dicedad, inplace=True)
    
    dfs = [pdnro, psexo, pedad]
    personas = reduce(lambda left, right: pd.merge(left,right,on='COD_ENCUESTAS'), dfs)
    
    personas = permpio.append(personas).fillna(0)
    
    return personas


def groupby_mode(result, *args):
    """
    Group DataFrame by MPIO, counts U_EDIFICA and other variables

    Parameters
    ----------
    result : pandas DataFrame
        DataFrame containing all data merged.
    *args : boolean, optional
        True --> Include age groups in the group by.

    Returns
    -------
    result_mode : pandas DataFrame
        DataFrame with the data grouped and mode applied to MATER variables.
    result_nedif : pandas DataFrame
        DataFrame with data grouped by MPIO, MATER.

    """
    try:
        
        if True in args:
            result_mode = result.groupby(["U_MPIO", "UA_CLASE", "U_SECT_RUR", "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA",\
                                "U_EDIFICA"]).agg({'THOG':['sum'], 'TPER':['sum'], 'V_MAT_PARED': func_mode,
                                      'V_MAT_PISO': func_mode, 'V_TIPO_VIV': func_mode_tviv, 'THOM':['sum'], 'TMUJ':['sum'], 
                                      'T00':['sum'], 'T05':['sum'], 'T10':['sum'], 'T15':['sum'], 'T20':['sum'], 
                                      'T25':['sum'], 'T30':['sum'], 'T35':['sum'], 'T40':['sum'], 'T45':['sum'], 
                                      'T50':['sum'], 'T55':['sum'], 'T60':['sum'], 'T65':['sum'], 'T70':['sum'], 
                                      'T75':['sum'], 'T80':['sum'], 'T85':['sum'], 'T90':['sum'], 'T95':['sum'], 'T100':['sum']}).reset_index()
                                                   
            result_mode.columns = result_mode.columns.get_level_values(0)                                     
            result_nedif = result_mode.groupby(["U_MPIO", "UA_CLASE", "U_SECT_RUR", "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA", "V_MAT_PARED",\
                                                "V_MAT_PISO", "V_TIPO_VIV"]).agg({"U_EDIFICA": ['count'], 'TPER':['sum'], 'THOG':['sum'], 'THOM':['sum'], 'TMUJ':['sum'], 
                                                'T00':['sum'], 'T05':['sum'], 'T10':['sum'], 'T15':['sum'], 'T20':['sum'], 
                                                'T25':['sum'], 'T30':['sum'], 'T35':['sum'], 'T40':['sum'], 'T45':['sum'], 
                                                'T50':['sum'], 'T55':['sum'], 'T60':['sum'], 'T65':['sum'], 'T70':['sum'], 
                                                'T75':['sum'], 'T80':['sum'], 'T85':['sum'], 'T90':['sum'], 'T95':['sum'], 'T100':['sum']}).reset_index()
            result_nedif.columns = result_nedif.columns.get_level_values(0)
        else:
                 
            result_mode = result.groupby(["U_MPIO", "UA_CLASE", "U_SECT_RUR", "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA",\
                                   "U_EDIFICA"]).agg({'THOG':['sum'], 'TPER':['sum'],"V_MAT_PARED": func_mode,
                                       "V_MAT_PISO": func_mode, 'V_TIPO_VIV': func_mode_tviv}).reset_index()
                                                      
            result_mode.columns = result_mode.columns.get_level_values(0) 
        
            result_nedif = result_mode.groupby(["U_MPIO", "UA_CLASE", "V_MAT_PARED",\
                                    "V_MAT_PISO", 'V_TIPO_VIV']).agg({"U_EDIFICA": ['count'], 'TPER':['sum'], 'THOG':['sum']}).reset_index()                                                                      
            result_nedif.columns = result_nedif.columns.get_level_values(0)
    except:

        pass                        

    return result_mode, result_nedif



def write_results(result_dptos, result_mode, result_nedif, filtClase, cod, codmpio, dptocod, resumen_mpios=None, *args):
    """
    Write the DataFrames containing the results

    Parameters
    ----------
    result_dptos : pandas DataFrame
        DataFrame containing results grouped by MAT.
    result_mode : pandas DataFrame
        DESCRIPTION.
    result_nedif : pandas DataFrame
        DESCRIPTION.
    filtClase : list
        DESCRIPTION.
    cod : int
        DESCRIPTION.
    codmpio : int
        DESCRIPTION.
    dptocod : int
        DESCRIPTION.
    resumen_mpios : pandas DataFrame, optional
        DataFrame containing results grouped by MPIO and age groups. The default is None.
    *args : boolean, optional
        True --> Include age groups in the group by.

    Returns
    -------
    result_dptos : pandas DataFrame
        DataFrame containing results grouped by MAT and with numerical values modified by strings.
    resumen_mpios : pandas DataFrame, optional
        DataFrame containing results grouped by MPIO and age groups. The default is None.

    """
    try:
        if True in args:
            
            if resumen_mpios is not None:
                resumen_mpios = resumen_mpios.append(result_mode[result_mode["UA_CLASE"].isin(filtClase)].groupby(["U_MPIO", "UA_CLASE", "U_SECT_RUR", "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA"
                                                     ]).agg({"U_EDIFICA": ['count'], 'TPER':['sum'], 'THOG':['sum'], 'THOM':['sum'], 'TMUJ':['sum'], 
                                                    'T00':['sum'], 'T05':['sum'], 'T10':['sum'], 'T15':['sum'], 'T20':['sum'], 
                                                    'T25':['sum'], 'T30':['sum'], 'T35':['sum'], 'T40':['sum'], 'T45':['sum'], 
                                                    'T50':['sum'], 'T55':['sum'], 'T60':['sum'], 'T65':['sum'], 'T70':['sum'], 
                                                    'T75':['sum'], 'T80':['sum'], 'T85':['sum'], 'T90':['sum'], 'T95':['sum'], 'T100':['sum']}).reset_index(), 
                                                    ignore_index=True)
                                                                                                
                result_nedifstr = result_nedif[result_nedif["UA_CLASE"].isin(filtClase)].copy() 

        else:
            result_nedif = result_mode.groupby(["U_MPIO", "V_MAT_PARED",\
                                    "V_MAT_PISO", 'V_TIPO_VIV']).agg({"U_EDIFICA": ['count'], 'TPER':['sum'], 'THOG':['sum']}).reset_index()                                                                      
            result_nedif.columns = result_nedif.columns.get_level_values(0)
            result_nedifstr = result_nedif.copy()
    except:
        print("Error while writing resumen results")
        
        pass
    
    #%%
    for i, row in result_nedifstr.iterrows():
        
        matpared = int(row["V_MAT_PARED"])
        matpiso  = int(row["V_MAT_PISO"])
        tvivienda  = int(row["V_TIPO_VIV"])
        
        mpisostr = cambio_variable('V_MAT_PISO_VS1', matpiso)
        mparedstr = cambio_variable('V_MAT_PARED_VS1', matpared)
        tviviendastr = cambio_variable('V_TIPO_VIV_VS1', tvivienda)
        
        result_nedifstr.loc[i, "Departamento"] = dptocod
        result_nedifstr.loc[i, "U_MPIO"] = codmpio
        result_nedifstr.loc[i, "COD"] = cod
        result_nedifstr.loc[i, "V_MAT_PARED"] = mparedstr
        result_nedifstr.loc[i, "V_MAT_PISO"] = mpisostr
        result_nedifstr.loc[i, "No. total edificaciones"] = result_nedif['U_EDIFICA'].sum()
        result_nedifstr.loc[i, "V_TIPO_VIV"] = tviviendastr
        
    result_dptos = result_dptos.append(result_nedifstr, ignore_index=True)
    
    if True in args:
        return result_nedifstr, result_dptos, resumen_mpios
    else:
        return result_nedifstr, result_dptos



def write_resumen(resumen_dptos, result_mode, result_nedif, mpio, cod):
    """
    Write a pandas DataFrame with a summary by municipality

    Parameters
    ----------
    resumen_dptos : pandas DataFrame
        DataFrame containing results grouped by MPIO.
    result_mode : pandas DataFrame
        DESCRIPTION.
    result_nedif : pandas DataFrame
        DESCRIPTION.
    mpio : pandas Series
        Municipality data.
    cod : int
        Code.

    Returns
    -------
    resumen_dptos : pandas DataFrame
        DataFrame containing results grouped by MPIO.

    """
    resumen_dptos = resumen_dptos.append({'Departamento': (mpio[1]["Departamento"]),
                                  'Cod': cod,
                                  'Personas C. Municipal': result_mode[result_mode["UA_CLASE"] == 1]["TPER"].sum(),
                                  'Personas C. Poblado': result_mode[result_mode["UA_CLASE"] == 2]["TPER"].sum(),
                                  'Personas Rural Disperso y Resto': result_mode[result_mode["UA_CLASE"].isin([3, 4])]["TPER"].sum(),
                                  'Total personas': result_nedif['TPER'].sum(),
                                   'Edificaciones C. Municipal': result_mode[result_mode["UA_CLASE"] == 1]["U_EDIFICA"].count(),
                                   'Edificaciones C. Poblado': result_mode[result_mode["UA_CLASE"] == 2]["U_EDIFICA"].count(),
                                   'Edificaciones Rural Disperso y Resto': result_mode[result_mode["UA_CLASE"].isin([3, 4])]["U_EDIFICA"].count(),
                                  'Total edificaciones': result_nedif['U_EDIFICA'].sum()
                                  }, ignore_index =True)
    return resumen_dptos


def func_principal(folder_path, deptcod, deptname, filtClase=[1, 2], filtUnidad=[1, 2], filtViv=[1, 2, 3], *args):
    """
    Principal function which iterate through any number of specified Departments.

    Parameters
    ----------
    folder_path : string (path)
        Path to folder which contains folders and DANE files.
    deptcod : int
        Code of the department to iterate.
    deptname : string
        Name of the department.
    filtClase : list
        List containing Clase filter options.
    filtUnidad : list
        List containing Uso filter options.
    filtViv : list
        List containing Tipo_Vivienda filter options.
    *args : booleans
        Two last paremeters ( , ). 1st position -> Specifies if consider age groups in the group by operations.
        2nd position -> Specifies if writes a municipality summary.

    Returns
    -------
    result_dptos : TYPE
        DESCRIPTION.
    resumen_dptos : TYPE
        DESCRIPTION.
    resumen_mpios : TYPE
        DESCRIPTION.
    result_nedifstr : TYPE
        DESCRIPTION.
    result_mode : TYPE
        DESCRIPTION.
    result_nedif : TYPE
        DESCRIPTION.

    """
    start = time.time()
    
    #%% Manejo y re arreglo de los datos    
    result_dptos = pd.DataFrame()
    resumen_dptos = pd.DataFrame()
    resumen_mpios = pd.DataFrame()
    for i in range(len(deptcod)):
        dptocod = deptcod[i]
        depto = deptname[i]
        
        print('Iterando Departamento:{}, Código: {}'.format(depto, dptocod))
        
        #%% Read MGN, VIV, PER, files from specified folder path
        
        mgn, viv, per, mpios_list = read_files(folder_path, dptocod, depto)
        
        #%% Filter data by CLASE, USO_UNIDAD, TIPO_VIVIENDA
        mgn, viv, per = filter_files(mgn, viv, per, filtUnidad=filtUnidad, filtViv=filtViv)
        mpios_list = mpios_list[mpios_list["Departamento"] == int(dptocod)]    
        
        #%%
        for mpio in mpios_list.iterrows():
            if dptocod[0] == '0':
                dig = 1
            else:
                dig = 2            
            mpoestudio = str(mpio[1]["COD"])[dig:].lstrip("0")
            mpoestudio = int(mpoestudio)
            
            if viv['U_MPIO'].isin([mpoestudio]).any():
                
                print('Iterando Municipio: {}'.format(mpoestudio))
                
                codmpio = str(mpio[1]["COD"])[dig:]
                cod = str(dptocod) + codmpio
                
                mgnestudio = mgn[mgn["U_MPIO"] == mpoestudio]
                vivestudio = viv[viv["U_MPIO"] == mpoestudio]
                perestudio = per[per["U_MPIO"] == mpoestudio]
                
                #%% Personas data is organized and stacked as VIV format
                
                personas = organize_personas(perestudio)                

                #%% MGV, VIV, PER dataframes are merged.
                    
                dfs = [vivestudio[["COD_ENCUESTAS", "V_MAT_PARED", "V_MAT_PISO", 'V_TIPO_VIV']],
                       mgnestudio[["COD_ENCUESTAS", "U_MPIO", "UA_CLASE", "U_SECT_RUR", "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA", \
                                  "U_EDIFICA", "COD_DANE_ANM"]],                   
                           personas]
                    
                result = reduce(lambda left,right: pd.merge(left,right,on='COD_ENCUESTAS', how='left'), dfs)
                
                result = result.drop_duplicates()
                
                result = result.fillna(0)
                
                #%% The data is grouped by desired fields. If optional arg is True data grouping will include number of people by age groups.
    
                #result_mode, result_nedif = groupby_mode(result, False)
                
                #%% Write and filter the results based on CLASE
                if True == args[0]:
                    result_mode, result_nedif = groupby_mode(result, True)
                    result_nedifstr, result_dptos, resumen_mpios = write_results(result_dptos, result_mode, result_nedif, filtClase, cod, codmpio, dptocod, resumen_mpios, True)
                    
                else:
                    result_mode, result_nedif = groupby_mode(result, False)
                    result_nedifstr, result_dptos = write_results(result_dptos, result_mode, result_nedif, filtClase, cod, codmpio, dptocod, None, False)
                
                if True == args[1]:
                    resumen_dptos = write_resumen(resumen_dptos, result_mode, result_nedif, mpio, cod)
                
                print('Terminado Municipio: {}'.format(mpoestudio))
    
    try:
        
        resumen_mpios.columns = resumen_mpios.columns.get_level_values(0)     
        resumen_mpios = resumen_mpios.rename(columns={'U_MPIO': 'Municipio',\
                                                      'U_EDIFICA': 'No. edificaciones'})  
            
    except:
        pass
        
    result_dptos = result_dptos.rename(columns={'U_MPIO': 'Municipio',\
                              'V_MAT_PARED': 'Material Pared',\
                              'V_MAT_PISO': 'Material Piso',
                              'V_TIPO_VIV': 'Tipo Vivienda',
                              'U_EDIFICA': 'No. edificaciones'})
    
    end = time.time()
    print('Ended in {}'.format(end-start))
    
    return result_dptos, resumen_dptos, resumen_mpios, result_nedifstr, result_mode, result_nedif
