#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 17:53:51 2021

@author: kuehbach
"""

import sys
#MYPREFIX='/media/kuehbach/Kvanefjeld02/THEOBOOK_165_FHI_FHI_FHI/FHI_FHI_FHI/Paper/xxxx_ParaprobeAnalyticsAsAFairMatPlugin/'
MYPREFIX='/home/kuehbach/HU_HU_HU/FAIRmatSoftwareDevelopment/Sprint01_NorthLauncher/'
sys.path.append(MYPREFIX)
#odsfile = 'Sprint01_NorthLauncher_SoftwareToolList_EM_02.ods'
#methodname = 'Electron microscopy'
#sheetname = "EM"
#odsfile = 'Sprint01_NorthLauncher_SoftwareToolList_ARPES_02.ods'
#methodname = 'Angle-resolved spectroscopy'
#sheetname = "ARPES"
#odsfile = 'Sprint01_NorthLauncher_SoftwareToolList_XPS_02.ods'
#methodname = 'Core-level spectroscopy'
#sheetname = "XPS"
#odsfile = 'Sprint01_NorthLauncher_SoftwareToolList_OPTICAL_02.ods'
#methodname = 'Optical spectroscopy'
#sheetname = "OPTICAL"
odsfile = 'Sprint01_NorthLauncher_SoftwareToolList_APM_02.ods'
methodname = 'Atom probe microscopy'
sheetname = "APM"


#import additional python things
import numpy as np
import h5py
import pandas as pd

def bold(string):
    return '**'+string+'**'

def hyperlink(string):
    return '<a href="' + string + '" target="_top">' + string + '</a>'

def doi(doistring):
    return '<a href="https://dx.doi.org/' + doistring + '" target="_top">https://dx.doi.org/' + doistring + '</a>'

def cellentry(cellstring):
    retval = ''
    if type(cellstring) == str:
        retval = '<th>'+cellstring+'</th>'
    elif type(cellstring) == int:
        retval = '<th>'+str(int(cellstring))+'</th>'
    else:
        retval = '<th></th>'
    return retval

#read concepts from ODS spreadsheet
tmp = pd.read_excel(MYPREFIX + odsfile, sheet_name = sheetname, engine="odf", keep_default_na=False, na_values=['_'] ) #, comment='#') #dont use hashmark for comments, Zenodo hashs may have these causing a line break and parsing problems
if sheetname == "EM":
    columnnames = tmp.columns.values.tolist()[:-1] #discard cryo-EM thingi
else:
    columnnames = tmp.columns.values.tolist()
linebreak = '<br>\n'

#expecting columns, ranking, name, description, link, doi, what, license, programming lanuages
#tablelayout = True
#colnm2colid = { 'Name': 1, 'Link': 2, 'License': 3, 'Importance': 4, 'Description': 5, 'Category': 6, 'Supported OS': 7, 'UserInterface': 8, 'Dependencies': 9 }
#odscolid2colnm = { 0: 'Importance', 1: 'Name', 2: 'Description', 3: 'Link', 4: 'DOI', 5: 'Category', 6: 'License', 7: Importance }

txt = '# ' + methodname + '<br>\n'
#if tablelayout == True:
#create table header
txt += '<table style="width:100%">'+linebreak
#txt += '| '
txt += '<tr>'+linebreak
for colnm in columnnames:
    #txt += string + ' | '
    txt += '<th>'+colnm+'</th>'+linebreak
#txt = txt.rstrip() + '<br>\n'
txt += '</tr>'+linebreak
#txt += '| '
#for colnm in columnnames:
#    txt += '---------------------' 
#    txt += ' | '
#txt = txt.rstrip() + '<br>\n'    
for rowidx in np.arange(2,tmp.shape[0]):
    #sheet layout
    txt += '<tr>'+linebreak
    #txt += '| '
    for colnm in columnnames:
        obj = tmp.iloc[rowidx, tmp.columns.get_loc(colnm)]
        if colnm == 'Link':
            txt += cellentry(hyperlink(obj))
        else:
            txt += cellentry(obj)
    txt += '</tr>'+linebreak
        #txt += ' | '
    #txt = txt.rstrip() + '<br>\n'
txt +='</table>'+linebreak
markdownfile = open(MYPREFIX + odsfile + '.md', 'wt')
n = markdownfile.write(txt)
markdownfile.close()

# =============================================================================
#        #plain text layout
#         txt += '### ' + tmp.iloc[r,1] + '<br>\n'
#         txt += tmp.iloc[r,2] + '<br>\n'
#         if type(tmp.iloc[r,3]) == str:
#             txt += 'Link: ' + hyperlink(tmp.iloc[r,3]) + '<br>\n'
#         else:
#             txt += 'Link: ' + '<br>\n'
#         if type(tmp.iloc[r,4]) == str:
#             txt += 'DOI: ' + doi(tmp.iloc[r,4]) + '<br>\n'
#         txt += 'Category: ' + tmp.iloc[r,5] + '<br>\n'
#         txt += 'License: ' + tmp.iloc[r,6] + '<br>\n'
#         txt += 'Importance: ' + str(int(tmp.iloc[r,0])) + '<br>\n'
#         if type(tmp.iloc[r,8]) == str:
#             txt += 'Current version: ' + tmp.iloc[r,8] + '<br>\n'
#         else:
#             txt += 'Current version: ' + '#tbd provided tool is integrated' + '<br>\n'
#         languages = ['Python','Matlab','R','C/C++','Java/JavaScript','Others']
#         speaks = ''
#         for i in np.arange(0,len(languages)):
#             if type(tmp.iloc[r,9+i]) == str:
#                 speaks += languages[i] + ', '
#         if speaks.endswith(', '):
#             speaks = speaks[:-2]
#         txt += 'Main programming languages: ' + speaks + '<br>\n'
# =============================================================================
