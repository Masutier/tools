import os
from django.contrib import messages
from django.shortcuts import render
from openpyxl import load_workbook
import pandas as pd


def xlsTool(request):
    nrowsx = 11
    # Revisar si el archivo existe
    if os.path.isfile('static/docs/xlsx_All.xlsx') == True:
        xlsxFile = pd.read_excel('static/docs/xlsx_All.xlsx', 'Top_All') # Lee el archivo de excel
        xlsxFile7 = pd.read_excel(
            io='static/docs/xlsx_All.xlsx',
            engine='openpyxl',
            sheet_name='Top_All',
            skiprows=0,
            nrows=nrowsx,
        )
        records = len(xlsxFile) - 1
        column_names=xlsxFile7.columns.values
        row_data=list(xlsxFile7.values.tolist())
        context={
            'column_names':column_names,
            'row_data':row_data,
            'records':records,
            'nrowsx':nrowsx,
            'title': "xlsx Home"
        }
        return render(request, 'xls_app/xlsTool.html', context)
    else:
        messages.info(request, 'El archivo principal no existe')
        return render(request, 'xls_app/createNewXls.html')


def excelTable(request):
    xlsxFile = pd.read_excel('static/docs/xlsx_All.xlsx', 'Top_All')
    xlsxFile7 = pd.read_excel(
        io='static/docs/xlsx_All.xlsx',
        engine='openpyxl',
        sheet_name='Top_All',
        skiprows=0,
    )
    records = len(xlsxFile) - 1
    column_names=xlsxFile7.columns.values
    row_data=list(xlsxFile7.values.tolist())
    context={
        'column_names':column_names,
        'row_data':row_data,
        'records':records,
        'title': "xlsx Main"
    }
    return render(request, 'xls_app/excelTable.html', context)


def duplicates(request):
    xlsxFile = pd.read_excel('static/docs/xlsx_All.xlsx', 'Top_All')
    duplicates = xlsxFile.loc[xlsxFile.duplicated('Nombre del Flujo'), :]
    column_names=duplicates.columns.values
    row_data=list(duplicates.values.tolist())
    context={
        'column_names':column_names,
        'row_data':row_data,
        'title': "xlsx Duplicados"
    }
    if not duplicates.empty:
        return render(request, 'xls_app/duplicates.html', context)
    else:
        messages.info(request, 'No hay registros duplicados')
        return redirect('/')


def createNewXls(request):
    if request.method == 'POST':
        if os.path.isfile('static/docs/xlsx_All.xlsx') == False:
            openFile = request.FILES['inputFirstXlsx'] # Llamar el primer archivo y guardarlo en docs
            newOneFile = pd.read_excel(openFile)
            newOneFile = newOneFile.drop_duplicates(keep='first') # borrar filas repetidas
            openFile = request.FILES['inputSecondXlsx'] # Llamar el segundo archivo y guardarlo en docs
            newTwoFile = pd.read_excel(openFile)
            newTwoFile = newTwoFile.drop_duplicates(keep='first') # borrar filas repetidas
            allDataMerge = pd.merge(newOneFile, newTwoFile, on='Nombre del Flujo', how='outer') # unir los archivos 
            allDataMerge['Total'] = allDataMerge.iloc[:, 1:12].sum(axis=1) # Sum columns
            allDataMerge.to_excel('static/docs/xlsx_All.xlsx', 'Top_All', index=False) # create and save xlsx_All.xlsx
            column_names=allDataMerge.columns.values
            row_data=list(allDataMerge.values.tolist())
            context = {
                'column_names':column_names,
                'row_data':row_data,
                'title': "xlsx crear"
            }
            return render(request, 'xls_app/excelTable.html', context)
    context={'title': "xlsx Main"}
    return render(request, 'xls_app/createNewXls.html', context)


def createAddXls(request):
    if request.method == 'POST':
        if os.path.isfile('static/docs/xlsx_All.xlsx') == True:
            newOneFile = pd.read_excel('static/docs/xlsx_All.xlsx', 'Top_All') # Lee el archivo de excel existente y borrar la columna Total
            newOneFile.drop('Total', axis=1, inplace=True)
            openFile = request.FILES['inputXlsx'] # Llamar el segundo archivo
            newTwoFile = pd.read_excel(openFile)
            newTwoFile = newTwoFile.drop_duplicates(keep='first') # borrar filas repetidas
            allFiles = pd.merge(newOneFile, newTwoFile, on='Nombre del Flujo', how='outer') # unir los archivos 
            allFiles['Total'] = allFiles.iloc[:, 1:12].sum(axis=1) # Sum columns
            allFiles = allFiles.drop_duplicates(keep='first') # borrar filas repetidas
            allFiles.to_excel('static/docs/xlsx_All.xlsx', 'Top_All', index=False) # create and save xlsx_All.xlsx
            column_names=allFiles.columns.values
            row_data=list(allFiles.values.tolist())
            context = {
                'column_names':column_names,
                'row_data':row_data,
                'title': "xlsx crear"
            }
            return render(request, 'xls_app/excelTable.html', context)
        else:
            messages.info(request, 'El archivo no existe')
            return render(request, 'xls_app/createNewXls.html')
    return render(request, 'xls_app/createAddXls.html')


def delXls(request):
    if request.method == 'POST':
        if os.path.isfile('static/docs/xlsx_All.xlsx') == True:
            os.remove('static/docs/xlsx_All.xlsx')
            messages.info(request, 'El archivo fue borrado')
        return render(request, 'xls_app/createNewXls.html')
    context = {'title': "xlsx Borrar Todo"}
    return render(request, 'xls_app/delXls.html', context)


def delColXls(request):
    nrowsx = 7
    # Revisar si el archivo existe
    if os.path.isfile('static/docs/xlsx_All.xlsx') == True:
        xlsxFile7 = pd.read_excel(
            io='static/docs/xlsx_All.xlsx',
            engine='openpyxl',
            sheet_name='Top_All',
            skiprows=0,
            nrows=nrowsx,
        )
        column_names=xlsxFile7.columns.values
        row_data=list(xlsxFile7.values.tolist())
        context={
            'column_names':column_names,
            'row_data':row_data,
            'title': "xlsx Borrar Columna"
        }
    else:
        messages.info(request, 'El archivo no existe')
        return render(request, 'xls_app/createNewXls.html')
    
    if request.method == 'POST':
        columnToDel = request.POST.get('inputColumn')
        xlsxFile = pd.read_excel('static/docs/xlsx_All.xlsx', 'Top_All') # Lee el archivo de excel existente
        xlsxFile.drop('Total', axis=1, inplace=True) # borrar la columna Total
        xlsxFile.drop(columnToDel, axis=1, inplace=True) # borrar la columna deseada
        xlsxFile['Total'] = xlsxFile.iloc[:, 1:12].sum(axis=1) # Sum columns
        xlsxFile.to_excel('static/docs/xlsx_All.xlsx', 'Top_All', index=False) # create and save xlsx_All.xlsx
        column_names=xlsxFile.columns.values
        row_data=list(xlsxFile.values.tolist())
        context = {
            'column_names':column_names,
            'row_data':row_data,
            'title': "xlsx Tabla"
        }
        messages.info(request, 'La Columna fue borrada')
        return render(request, 'xls_app/excelTable.html', context)
    return render(request, 'xls_app/delCol.html', context)
