import json
import os
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pdf2image import convert_from_path, convert_from_bytes
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfReader
from .utils import *

destiny_path = "/home/gabriel/Downloads/catalogRossy/destiny/"
origen_path = "/home/gabriel/Downloads/catalogRossy/"


def pdfTool(request):
    catalogList = []
    path = (destiny_path)
    chkFolder = os.path.isdir(path)
    if not chkFolder:
        messages.info(request, 'El archivo no existe')
        return redirect('/pdfLoad')
    else:
        catalogList = os.listdir(path)
        catalogList.sort()
        context = {"title": "pdf", 'catalogList': catalogList, 'abs_path':path}
        return render(request, 'pdf_app/pdfTool.html', context)


# brake down pdf into jpg images
def pdfLoad(request):
    count += 1
    count1 = 0
    count2 = 100
    count3 = 200
    catalogList = []

    if request.method == 'POST':
        pdfFile = request.FILES['inputPdf']
        user_answer = request.POST['exampleRadios']
        month = request.POST['mes']
        nameFile = pdfFile.name
        fileNamex = nameFile.split('.')
        file_tp_pross = origen_path + nameFile

        #OPEN FILE
        with open(file_tp_pross, "rb") as f:
            reader = PdfFileReader(f)

            if len(reader.pages) > 180 or len(reader.pages) < 300:
                part1 = PdfFileWriter()
                part2 = PdfFileWriter()
                part3 = PdfFileWriter()

                first = list(range(0, 100))
                second = list(range(100, 200))
                third = list(range(200, 300))

                for page in range(len(reader.pages)):
                    if page in first:
                        count1 += 1
                        part1.addPage(reader.getPage(page))

                    if page in second:
                        count2 += 1
                        part2.addPage(reader.getPage(page))

                    if page in third:
                        count3 += 1
                        part3.addPage(reader.getPage(page))

                if part1:
                    with open(origen_path + "/" + "part1.pdf", "wb") as f2:
                        part1.write(f2)

                if part2:
                    with open(origen_path + "/" + "part2.pdf", "wb") as f3:
                        part2.write(f3)

                if part3:
                    with open(origen_path + "/" + "part3.pdf", "wb") as f4:
                        part3.write(f4)

                if user_answer == "Compu":
                    crearFolder(destiny_path, fileNamex, month)
                    part1Pdf = convert_from_path(origen_path + "part1.pdf", dpi=800)
                    for idx, imag in enumerate(part1Pdf):
                        if imag.width > 800:
                            new_img = (800, None)
                            imag.save(destiny_path + fileNamex[0] + "_" + month + "/" + fileNamex[0] + "_" + str(count) + '.jpg', 'JPEG', quality=95)
                        else:
                            imag.save(destiny_path + fileNamex[0] + "_" + month + "/" + fileNamex[0] + "_" + str(count) + '.jpg', 'JPEG', quality=95)

                    return redirect('/pdfTool')

    return render(request, 'pdf_app/pdfLoad.html')


# create pdf from html
def createPdf(request):
    empInfo = [
        {'name': 'Bob', 'job': 'Manager'},
        {'name': 'Kim', 'job': 'Developer'},
        {'name': 'Sam', 'job': 'Developer'},
        {'name': 'Erika', 'job': 'CEO'},
        {'name': 'Eustacio', 'job': 'Developer'},
        {'name': 'Rosalba', 'job': 'Developer'},
        {'name': 'Julieta', 'job': 'Asistente'}
    ]
    pdf = render_to_pdf('pdf_app/htmlToPdf.html', {'empInfo':empInfo})
    return HttpResponse(pdf, content_type='application/pdf')


def ordenCompraDownloadPDF(request):
    now = datetime.now()
    x = now.strftime("%m_%d_%Y")
    empInfo = [
        {'name': 'Bob', 'job': 'Manager'},
        {'name': 'Kim', 'job': 'Developer'},
        {'name': 'Sam', 'job': 'Developer'},
        {'name': 'Erika', 'job': 'CEO'},
        {'name': 'Eustacio', 'job': 'Developer'},
        {'name': 'Rosalba', 'job': 'Developer'},
        {'name': 'Julieta', 'job': 'Asistente'}
    ]
    pdf = render_to_pdf('pdf_app/htmlToPdf.html', {'empInfo':empInfo})
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = 'OC_all_%s.pdf' %x
    content = "attachment; filename=%s" %(filename)
    response['Content-Disposition'] = content
    return response
