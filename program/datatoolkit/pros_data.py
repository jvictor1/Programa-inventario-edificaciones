# -*- coding: utf-8 -*-
"""
    Created on Wed Sep 30 09:30:17 2020

    @author: Juan Camilo Victoria & Santiago Sepúlveda
    versión actualizada 13/06/2022
    
    Módulo que tiene como función principal el manejo de los datos del CENSO.
    Para esto, la clase ProcessTheData contiene los métodos necesarios para
    leer, procesar y escribir.
    
    ProcessTheData: Permite crear una instancia para el procesamiento de los datos del censo
    
    Los argumentos de entrada:
        
        folder_path: Ruta a la carpeta en la que se encuentran los arhivos CSV.
        departments_index: Índice que corresponde a los departamentso que se desean analizar.
        filters: Filtros deseados a aplicar durante el procesamiento.
                (Filtro por clase -> List of integers, filtro por unidad -> List of integers, filtro por vivienda -> List of integers)
        extra_options: Booleans que le permite a la instancia ejecutar o no.
                (Agrupar por edad ->True/False, Ejecutar resumen-> True/False)
    
    



"""

from __future__ import division
import numpy as np
import pandas as pd
import time
from functools import reduce
import os
import datatoolkit.utilities as ut
from datatoolkit.departamentos import Departamentos


#%% Clase -> procesar datos del censo
class ProcessTheData(Departamentos):
    
    def __init__(self, folder_path, departments_index, filters, extra_options):
        
        #Initialize instance variables
        self.folder_path       = folder_path
        Departamentos.__init__(self, departments_index)
        # self.departments_index = departments_index
        self.filter_clase      = filters[0]
        self.filter_unidad     = filters[1]
        self.filter_vivienda   = filters[2]
        self.group_by_ages     = extra_options[0]
        self.do_resumen        = extra_options[1]
        
        #Execute main functions
        
        #Read
        mgn_list, viv_list, per_list, mpios_list = self._read_files()
        #Filter
        # print(viv_list[0].columns)
        mgn_filtered_list, viv_filtered_list, per_filtered_list = self._filter_files(mgn_list, viv_list, per_list)
        #Main iteration
        self.main(mgn_filtered_list, viv_filtered_list, per_filtered_list, mpios_list);
        
        
        
    
#%% Funciones
    def save_results(self, save_path=''):
        """
        Save the result DataFrames in csv format and store the path

        Parameters
        ----------
        save_path : optional 
            path to desired save folder.
        Returns
        -------
        None.

        """
        self.df_merged_mode.to_csv(save_path + "df_merged_mode.csv", index=False)
        self.df_merged_nedif.to_csv(save_path + "df_merged_nedif.csv", index=False)
        self.df_merged_nedifstr.to_csv(save_path + "df_merged_nedifstr.csv", index=False)
        
        self.df_result_departments.to_csv(save_path + "df_result_departments.csv", index=False)
        self.df_resumen_departments.to_csv(save_path + "df_resumen_departments.csv", index=False)
        self.df_resumen_municipios.to_csv(save_path + "df_resumen_municipios.csv", index=False) #Might by empty according to initiliazed arguments
        
        return 
        

    @staticmethod
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
        TVIV = {0: 'Sin informacion',
                1: 'Casa',
                2: 'Apartamento',
                3: 'Tipo Cuarto'}
        
        MPARED = {0: 'Sin informacion',
                  1: 'Bloque, ladrillo, piedra, madera pulida',
                  2: 'Concreto vaciado',
                  3: 'Material prefabricado',
                  4: 'Guadua',
                  5: 'Tapia pisada, bahareque, adobe',
                  6: ' Madera burda, tabla, tablon',
                  7: 'Cana, esterilla, otros vegetales',
                  8: 'Materiales de deshecho (Zinc, tela, carton, latas, plasticos, otros)',
                  9: 'No tiene paredes'}
        
        MPISO = {0: 'Sin informacion',
                 1: 'Marmol, parque, madera pulida y lacada',
                 2: 'Baldosa, vinilo, tableta, ladrillo, laminado',
                 3: 'Alfombra',
                 4: 'Cemento, gravilla',
                 5: 'Madera burda, tabla, tablon, otro vegetal',
                 6: 'Tierra, arena, barro'}
        
        ESTTO = {0: 'Sin Estrato',
                 1: 'Estrato 1',
                 2: 'Estrato 2',
                 3: 'Estrato 3',
                 4: 'Estrato 4',
                 5: 'Estrato 5',
                 6: 'Estrato 6',
                 9: 'No sabe el estrato',
                 10: 'Sin informacion'}
    
        
        if var == 'V_TIPO_VIV_VS1':
            
            return TVIV[idx]
        
        elif var == 'V_MAT_PARED_VS1':
            
            return MPARED[idx]
        
        elif var == 'V_MAT_PISO_VS1':
            
            return MPISO[idx]
        
        elif var == 'VA1_ESTRATO_VS1':
            
            return ESTTO[idx]
    
    @staticmethod
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
            
    @staticmethod
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
        
    def _read_files(self):
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
        mgn_list = []
        viv_list = []
        per_list = []
        
        #Reads each of the files of interest from the folder path and store them in a list
        for index in range(self.number_of_analyse):
            
            dpto_code = self.codes_analyse[index]
            dpto_name = self.names_analyse[index]
            
            filepath = self.folder_path + '/{}/'.format(str(dpto_code) + dpto_name)
            f_mgn = r"CNPV2018_MGN_A2_{}.CSV".format(dpto_code)
            f_viv = r"CNPV2018_1VIV_A2_{}.CSV".format(dpto_code)
            f_per = r"CNPV2018_5PER_A2_{}.CSV".format(dpto_code)
                
            mgn_list.append(pd.read_csv(filepath + f_mgn))
            viv_list.append(pd.read_csv(filepath + f_viv))
            per_list.append(pd.read_csv(filepath + f_per))
        
        mpios_list = pd.read_csv(os.path.dirname(ut.__file__) + '/mpios_list.csv', encoding="ISO-8859-1")
        
        return mgn_list, viv_list, per_list, mpios_list


    def _filter_files(self, mgn_list, viv_list, per_list):
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
        mgn_filtered_list = []
        viv_filtered_list = []
        per_filtered_list = []
        for index in range(self.number_of_analyse):
            
            #Retrieve each dataframe for each department
            mgn = mgn_list[index]
            viv = viv_list[index]
            per = per_list[index]
            
            # Fill NaN values with int values to handle them
            viv['V_MAT_PARED'] = viv['V_MAT_PARED'].fillna(0)
            viv['V_MAT_PISO'] = viv['V_MAT_PISO'].fillna(0)
            viv['VA1_ESTRATO'] = viv['VA1_ESTRATO'].fillna(10)
            per["P_NROHOG"] = per["P_NROHOG"].fillna(1)
            
            try:
                "An error will occur if the filter input parameter is different from a list"
                
                ## Cabecera Municipal clase = 1 Centro Poblado clase = 2
                #Filter MGN, VIV, PER data by CLASE
                if self.filter_clase:
                    
                    mgn = mgn[mgn["UA_CLASE"].isin(self.filter_clase)]
                    viv = viv[viv["UA_CLASE"].isin(self.filter_clase)]
                    per = per[per["UA_CLASE"].isin(self.filter_clase)]
                
                #Filter VIV data by USO_UNIDAD and TIPO_VIV
                viv = viv[viv['UVA_USO_UNIDAD'].isin(self.filter_unidad)] #Uso vivienda y uso mixto
                viv = viv[viv['V_TIPO_VIV'].isin(self.filter_unidad)]  #Tipo vivienda Casa Apartamento Cuarto
            except:
                pass    
            
            mgn_filtered_list.append(mgn)
            viv_filtered_list.append(viv)
            per_filtered_list.append(per)
            
        
        return mgn_filtered_list, viv_filtered_list, per_filtered_list

    @staticmethod
    def _format_personas(perestudio):
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


    def _group_by_mode(self, df_merged):
        """
        Group DataFrame by MPIO, counts U_EDIFICA and other variables
    
        Parameters
        ----------
        df_merged : pandas DataFrame
            DataFrame containing all dataFrames merged by municipio.
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
            
            if self.group_by_ages:
                df_merged_mode = df_merged.groupby(["U_MPIO", "UA_CLASE", "U_SECT_RUR", "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA",\
                                    "U_EDIFICA"]).agg({'THOG':['sum'], 'TPER':['sum'], 'V_MAT_PARED': ProcessTheData.func_mode,
                                          'V_MAT_PISO': ProcessTheData.func_mode, 'V_TIPO_VIV': ProcessTheData.func_mode_tviv, 'VA1_ESTRATO':ProcessTheData.func_mode, 'THOM':['sum'], 'TMUJ':['sum'], 
                                          'T00':['sum'], 'T05':['sum'], 'T10':['sum'], 'T15':['sum'], 'T20':['sum'], 
                                          'T25':['sum'], 'T30':['sum'], 'T35':['sum'], 'T40':['sum'], 'T45':['sum'], 
                                          'T50':['sum'], 'T55':['sum'], 'T60':['sum'], 'T65':['sum'], 'T70':['sum'], 
                                          'T75':['sum'], 'T80':['sum'], 'T85':['sum'], 'T90':['sum'], 'T95':['sum'], 'T100':['sum']}).reset_index()
                                                       
                df_merged_mode.columns = df_merged_mode.columns.get_level_values(0)                                     
                df_merged_nedif = df_merged_mode.groupby(["U_MPIO", "UA_CLASE", "U_SECT_RUR", "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA", "V_MAT_PARED",\
                                                    "V_MAT_PISO", "V_TIPO_VIV", 'VA1_ESTRATO']).agg({"U_EDIFICA": ['count'], 'TPER':['sum'], 'THOG':['sum'], 'THOM':['sum'], 'TMUJ':['sum'], 
                                                    'T00':['sum'], 'T05':['sum'], 'T10':['sum'], 'T15':['sum'], 'T20':['sum'], 
                                                    'T25':['sum'], 'T30':['sum'], 'T35':['sum'], 'T40':['sum'], 'T45':['sum'], 
                                                    'T50':['sum'], 'T55':['sum'], 'T60':['sum'], 'T65':['sum'], 'T70':['sum'], 
                                                    'T75':['sum'], 'T80':['sum'], 'T85':['sum'], 'T90':['sum'], 'T95':['sum'], 'T100':['sum']}).reset_index()
                df_merged_nedif.columns = df_merged_nedif.columns.get_level_values(0)
            else:
                     
                df_merged_mode = df_merged.groupby(["U_MPIO", "UA_CLASE", "U_SECT_RUR", "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA",\
                                       "U_EDIFICA"]).agg({'THOG':['sum'], 'TPER':['sum'], "V_MAT_PARED": ProcessTheData.func_mode,
                                           "V_MAT_PISO": ProcessTheData.func_mode, 'V_TIPO_VIV': ProcessTheData.func_mode_tviv, 'VA1_ESTRATO': ProcessTheData.func_mode}).reset_index()
                                                          
                df_merged_mode.columns = df_merged_mode.columns.get_level_values(0) 
            
                df_merged_nedif = df_merged_mode.groupby(["U_MPIO", "UA_CLASE", "V_MAT_PARED",
                                                                        "V_MAT_PISO", 'V_TIPO_VIV', 'VA1_ESTRATO']).agg({"U_EDIFICA": ['count'], 'TPER': ['sum'], 'THOG': ['sum']}).reset_index()
                df_merged_nedif.columns = df_merged_nedif.columns.get_level_values(0)
        except Exception as e:
            print(e)
            pass
        
        # self.merged_dataframe_mode = merged_dataframe_mode
        # self.merged_dataframe_nedif = merged_dataframe_nedif
    
        return df_merged_mode, df_merged_nedif



    def write_results(self, df_merged_dptos, df_merged_mode, df_merged_nedif, code, df_merged_resumen):
        """
        Write the DataFrames containing the results
    
        Parameters
        ----------
        result_dptos : pandas DataFrame
            DataFrame containing results grouped by MAT.
        df_merged_mode : pandas DataFrame
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
            if self.group_by_ages:
                
                if df_merged_resumen.empty != False:
                    df_merged_resumen = df_merged_resumen.append(df_merged_mode[df_merged_mode["UA_CLASE"].isin(self.filter_clase)].groupby(["U_MPIO", "UA_CLASE", "U_SECT_RUR", 
                                                                                                                       "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA"
                                                         ]).agg({"U_EDIFICA": ['count'], 'TPER':['sum'], 'THOG':['sum'], 'THOM':['sum'], 'TMUJ':['sum'], 
                                                        'T00':['sum'], 'T05':['sum'], 'T10':['sum'], 'T15':['sum'], 'T20':['sum'], 
                                                        'T25':['sum'], 'T30':['sum'], 'T35':['sum'], 'T40':['sum'], 'T45':['sum'], 
                                                        'T50':['sum'], 'T55':['sum'], 'T60':['sum'], 'T65':['sum'], 'T70':['sum'], 
                                                        'T75':['sum'], 'T80':['sum'], 'T85':['sum'], 'T90':['sum'], 'T95':['sum'], 'T100':['sum']}).reset_index(), 
                                                        ignore_index=True)
                                                                                                    
                    df_merged_nedifstr = df_merged_nedif[df_merged_nedif["UA_CLASE"].isin(self.filter_clase)].copy() 
    
            else:
                df_merged_mode = df_merged_mode[df_merged_mode["UA_CLASE"].isin(self.filter_clase)]
                df_merged_nedif = df_merged_mode.groupby(["U_MPIO", "V_MAT_PARED",\
                                        "V_MAT_PISO", 'V_TIPO_VIV', 'VA1_ESTRATO']).agg({"U_EDIFICA": ['count'], 'TPER':['sum'], 'THOG':['sum']}).reset_index()                                                                      
                df_merged_nedif.columns = df_merged_nedif.columns.get_level_values(0)
                
                df_merged_nedifstr = df_merged_nedif.copy()
        except:
            print("Error while writing resumen results")
            
            pass
        
        #%%
        
        df_merged_nedifstr.insert(0, 'cod', code)
        
        if len(df_merged_nedif) != 0:
        
            df_merged_nedifstr.loc[:, "No. total edificaciones"] = df_merged_nedif['U_EDIFICA'].sum()
            
            df_merged_nedifstr.loc[:, 'V_MAT_PARED'] = \
                df_merged_nedifstr.loc[:, 'V_MAT_PARED'].apply(lambda x: ProcessTheData.cambio_variable('V_MAT_PARED_VS1', int(x))).to_list()
        
            df_merged_nedifstr.loc[:, 'V_MAT_PISO'] = \
                df_merged_nedifstr.loc[:, 'V_MAT_PISO'].apply(lambda x: ProcessTheData.cambio_variable('V_MAT_PISO_VS1', int(x))).to_list()
        
            df_merged_nedifstr.loc[:, 'V_TIPO_VIV'] = \
                df_merged_nedifstr.loc[:, 'V_TIPO_VIV'].apply(lambda x: ProcessTheData.cambio_variable('V_TIPO_VIV_VS1', int(x))).to_list()
        
            df_merged_nedifstr.loc[:, 'VA1_ESTRATO'] = \
                df_merged_nedifstr.loc[:, 'VA1_ESTRATO'].apply(lambda x: ProcessTheData.cambio_variable('VA1_ESTRATO_VS1', int(x))).to_list()
            
            
        df_merged_dptos = df_merged_dptos.append(df_merged_nedifstr, ignore_index=True)
        

        return df_merged_nedifstr, df_merged_dptos, df_merged_resumen


    @staticmethod
    def write_resumen(df_merged_resumen, df_merged_mode, df_merged_nedif, mpio, cod):
        """
        Write a pandas DataFrame with a summary by municipality
    
        Parameters
        ----------
        df_merged_resumen : pandas DataFrame
            DataFrame containing summary by MPIO.
        df_merged_mode : pandas DataFrame
            DESCRIPTION.
        df_merged_nedif : pandas DataFrame
            DESCRIPTION.
        mpio : pandas Series
            Municipality data.
        cod : int
            Code.
    
        Returns
        -------
        df_merged_dptos : pandas DataFrame
            DataFrame containing results grouped by MPIO.
    
        """
        df_merged_resumen = df_merged_resumen.append({'Departamento': (mpio[1]["Departamento"]),
                                      'Cod': cod,
                                      'Personas C. Municipal': df_merged_mode[df_merged_mode["UA_CLASE"] == 1]["TPER"].sum(),
                                      'Personas C. Poblado': df_merged_mode[df_merged_mode["UA_CLASE"] == 2]["TPER"].sum(),
                                      'Personas Rural Disperso y Resto': df_merged_mode[df_merged_mode["UA_CLASE"].isin([3, 4])]["TPER"].sum(),
                                      'Total personas': df_merged_nedif['TPER'].sum(),
                                       'Edificaciones C. Municipal': df_merged_mode[df_merged_mode["UA_CLASE"] == 1]["U_EDIFICA"].count(),
                                       'Edificaciones C. Poblado': df_merged_mode[df_merged_mode["UA_CLASE"] == 2]["U_EDIFICA"].count(),
                                       'Edificaciones Rural Disperso y Resto': df_merged_mode[df_merged_mode["UA_CLASE"].isin([3, 4])]["U_EDIFICA"].count(),
                                      'Total edificaciones': df_merged_nedif['U_EDIFICA'].sum()
                                      }, ignore_index =True)
        return df_merged_resumen


    def main(self, mgn_filtered_list, viv_filtered_list, per_filtered_list, mpios_list):
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
        
        for i in range(len(self.codes_analyse)):
            
            dptocod = self.codes_analyse[i]
            depto = self.names_analyse[i]
            
            print('Iterando Departamento:{}, Código: {}'.format(depto, dptocod))
            
            #%% Read MGN, VIV, PER, files from specified folder path
            
            mgn = mgn_filtered_list[i]
            viv = viv_filtered_list[i]
            per = per_filtered_list[i]
            
            mpios_analyse = mpios_list[mpios_list["Departamento"] == int(dptocod)]    
            
            #%%
            for mpio in mpios_analyse.iterrows():
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
                    
                    personas = ProcessTheData._format_personas(perestudio)         
    
                    #%% MGV, VIV, PER dataframes are merged.
                        
                    dfs = [vivestudio[["COD_ENCUESTAS", "V_MAT_PARED", "V_MAT_PISO", 'V_TIPO_VIV', 'VA1_ESTRATO']],
                           mgnestudio[["COD_ENCUESTAS", "U_MPIO", "UA_CLASE", "U_SECT_RUR", "U_SECC_RUR", "UA2_CPOB", "U_SECT_URB", "U_SECC_URB", "U_MZA", \
                                      "U_EDIFICA", "COD_DANE_ANM"]],                   
                               personas]
                        
                    result = reduce(lambda left,right: pd.merge(left,right,on='COD_ENCUESTAS', how='left'), dfs)
                    
                    result = result.drop_duplicates()
                    
                    result = result.fillna(0)
                    
                    #%% The data is grouped by desired fields. If optional arg is True data grouping will include number of people by age groups.
        
                    #result_mode, result_nedif = groupby_mode(result, False)
                    
                    #%% Write and filter the results based on CLASE
                    result_mode, result_nedif = self._group_by_mode(result)
                    result_nedifstr, result_dptos, resumen_mpios = self.write_results(result_dptos, result_mode, result_nedif, cod, resumen_mpios)

                    if self.do_resumen:
                        resumen_dptos = ProcessTheData.write_resumen(resumen_dptos, result_mode, result_nedif, mpio, cod)
                    
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
                                  'U_EDIFICA': 'No. edificaciones',
                                  'VA1_ESTRATO': 'Estrato'})
        
        
        end = time.time()
        print('Elapsed time: {} s'.format(end-start))
        
        #Set instance result variables
        
        self.df_result_departments = result_dptos
        self.df_resumen_departments = resumen_dptos
        self.df_resumen_municipios  = resumen_mpios #Might by empty according to initiliazed arguments
        self.df_merged_nedifstr = result_nedifstr
        self.df_merged_mode     = result_mode
        self.df_merged_nedif    = result_nedif
        
        return
