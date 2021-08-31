# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 11:50:34 2021

@author: Juan Camilo Victoria & Santiago Sepúlveda
"""

import pandas as pd
import unidecode

def nvalxmat(csv, col, val):
    """
    Makes a pivot table to know number of buildings/people/homes grouped by material of wall/floor or building type

    Parameters
    ----------
    csv : pandas DataFrame
        CSV file which contains number of buildings by material combination.
    col : string
        maybe any of "Material Pared", "Material Piso", "Tipo Vivienda".
    val : string
        maybe any of "No. edificaciones", "TPER", "THOG".

    Returns
    -------
    None.

    """
    
    file = "{}.csv".format(csv)
    csv_file = pd.read_csv(r"{}".format(file))
    
    pivot = csv_file.pivot_table(index=["COD"], columns=[col], values=val, 
                  aggfunc = "sum", fill_value = 0).reset_index()

    return pivot

def changetilde(df):
    
    cols = ["Material Pared", "Material Piso", "Tipo Vivienda"]
    for col in cols:
        df.loc[:, col] = df.loc[:, col].apply(lambda row: unidecode.unidecode(row))
        
    return df

def save_csv(result, name):
    """
    Save any DataFrame in csv format

    Parameters
    ----------
    result : pandas DataFrame
        DESCRIPTION.
    name : string
        DESCRIPTION.

    Returns
    -------
    None.

    """
    result.to_csv("{}.csv".format(name), index=False)
    
    return

def setmax(df):
    """
    Set to 1 the typology with maximum number of buildings of the 'tiporesumen' output. 
    Helps to identify and to plot in maps the most common typology.

    Parameters
    ----------
    df : pandas DataFrame
        DataFrame with typology by municipality.

    Returns
    -------
    vis_data : pandas DataFrame
        DESCRIPTION.

    """
    idxmax_row = df.iloc[:, 2:].idxmax(axis=1)
    vis_data = df.copy()
    vis_data.iloc[:, 2:] = 0
    
    for i, row in vis_data.iterrows():
        vis_data.loc[i, idxmax_row[i]] = 1.0
    
    return vis_data

def cutstr(string):
    if string.split('/')[-1][0] == 'H':
        name = "/".join(string.split('/')[:-1])
    else:
        name = string
    return name

def aggregate(tipo, mza=False):
    """
    Aggregates typologies by all number of storeys.

    Parameters
    ----------
    tipo : pandas DataFrame
        'tipologias' DataFrame output.

    Returns
    -------
    data_unique : pandas DataFrame
        DataFrame with number of buildings by typology aggregated by number of storeys.
    """
    idx = tipo.columns.get_loc('ADO|EU/LWAL+DNO/H:1')
    colnames = tipo.columns.tolist()
    tiponames = tipo.columns.tolist()
    for i in range(len(colnames[idx:])):
        colnames[i+idx] = cutstr(colnames[i+idx])
        
    colnames = list(dict.fromkeys(colnames))
    
    data_unique = tipo.copy()
    data_unique = data_unique.drop(tiponames[idx:], axis=1)
    data_unique[colnames[idx:]] = 0
    for col in colnames[idx:]:
        for k, row in tipo.iterrows():
            for j in tiponames[idx:]:
                if col == cutstr(j):
                    data_unique.loc[k, col] = data_unique.loc[k, col] + row[j]
    return data_unique

colorlist = ["forestgreen",
             "darkorange",
             "cornflowerblue",
             "lime",
             "seagreen",
             "springgreen",
             "slateblue",
             "lightcoral",
             "khaki",
             "darkslategrey",
             "darkcyan",
             "olive",
             "orangered",
             "sienna",
             "sandybrown",
             "crimson",
             "tomato",
             "firebrick",
             "goldenrod",
             "mediumpurple",
             "chocolate"]

def qgisRuleSymbology(fieldi, nrange, colorlist):
    """
    Function to set rules symbology in QGIS layer. Works with 'setmax' output.
    This function opnly works in the QGIS python console.
    
    Parameters
    ----------
    fieldi : int
        Number of the initial field to set the rule.
    nrange : int
        Number fields to consider in the rules.
    colorlist : list
        List with color names that will be related with each rule.

    Returns
    -------
    None.

    """
    layer = iface.activeLayer()
    
    fields = []
    for field in layer.fields():
        field_name = field.name()
        fields.append(field_name)
    
    rules = []
    for i in range(nrange):
        label = fields[fieldi+i].split("_")[-1]
        rules.append(('{}'.format(label), '"' + fields[fieldi+i] + '"' + '= 1', colorlist[i], None))

    #$$ Create new symbology
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    renderer = QgsRuleBasedRenderer(symbol)
    # get the "root" rule
    root_rule = renderer.rootRule()
    for label, expression, color_name, scale in rules:
        print(label, expression, color_name, scale)
        # create a clone (i.e. a copy) of the default rule
        rule = root_rule.children()[0].clone()
        # set the label, expression and color
        rule.setLabel(label)
        rule.setFilterExpression(expression)
        rule.symbol().setColor(QColor(color_name))
        # set the scale limits if they have been specified
        if scale is not None:
            rule.setScaleMinDenom(scale[0])
            rule.setScaleMaxDenom(scale[1])
        # append the rule to the list of rules
        root_rule.appendChild(rule)
    
    # delete the default rule
    root_rule.removeChildAt(0)
    
    # apply the renderer to the layer
    layer.setRenderer(renderer)
    
    return


