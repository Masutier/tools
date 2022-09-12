from django.test import TestCase

def home():
    nrowsx = 7
    # Revisar si el archivo existe
    if os.path.isfile('static/docs/xlsx_All.xlsx') == True:
        xlsxFile = pd.read_excel('static/docs/xlsx_All.xlsx', 'Top_All')
        # Lee el archivo de excel
        xlsxFile7 = pd.read_excel(
            io='static/docs/xlsx_All.xlsx',
            engine='openpyxl',
            sheet_name='Top_All',
            skiprows=0,
            nrows=nrowsx,
        )
        records = len(xlsxFile) - 1
        return render('index.html', column_names=xlsxFile7.columns.values, row_data=list(xlsxFile7.values.tolist()), zip=zip, records=records)
    else:
        flash('El archivo no existe')
        return render('/excelFiles/createNew.html')
    return render('index.html')
