def pdfLoadTest(request):
    count = 0
    catalogList = []
    abs_path = 'static/docs/catalog/'

    if request.method == 'POST':
        pdfFile = request.FILES['inputPdf']
        user_answer = request.POST['exampleRadios']
        month = request.POST['mes']
        nameFile = pdfFile.name
        fileNamex = nameFile.split('.')
        images = convert_from_bytes(open(nameFile, 'rb').read())

        if user_answer == "AllSave":
            print("DRIVE")
            return redirect('/pdfTool')


        if user_answer == "Compu":
            print("COMPUTER")

            return redirect('/pdfTool')
            
    return render(request, 'pdf_app/pdfLoad.html')