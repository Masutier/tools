def createAddXls(request):
    if request.method == 'POST':
        if os.path.isfile('static/docs/xlsx_All.xlsx') == True:

            # Lee el archivo de excel existente y borrar la columna Total
            newOneFile = pd.read_excel('static/docs/xlsx_All.xlsx', 'Top_All')
            newOneFile.drop('Total', axis=1, inplace=True)

            openFile = request.FILES['inputXlsx']
            newTwoFile = pd.read_excel(openFile)

            # outer merge los archivos 
            allFiles = pd.merge(newOneFile, newTwoFile, on='Nombre del Flujo', how='outer')
            allFiles['Total'] = allFiles.iloc[:, 1:12].sum(axis=1)
            allFiles = allFiles.drop_duplicates(keep='first')

            # create and save xlsx_All.xlsx
            allFiles.to_excel('static/docs/xlsx_All.xlsx', 'Top_All', index=False)
            
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