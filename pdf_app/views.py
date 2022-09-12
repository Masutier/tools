import json
import os
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pdf2image import convert_from_path, convert_from_bytes
from .utils import *

destiny_path = "/home/gabriel/Downloads/catalogRossy/destiny/"
origen_path = "/home/gabriel/Downloads/"


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
    count = 0
    catalogList = []

    if request.method == 'POST':
        pdfFile = request.FILES['inputPdf']
        user_answer = request.POST['exampleRadios']
        month = request.POST['mes']
        nameFile = pdfFile.name
        fileNamex = nameFile.split('.')
        images = convert_from_bytes(open(origen_path + nameFile, 'rb').read())

        if user_answer == "AllSave":
            crearFolder(destiny_path, fileNamex, month)
            if len(images) <= 100:
                for imag in images:
                    count += 1
                    if imag.width > 1000:
                        new_img = (1000, None)
                        imag.save(destiny_path + fileNamex[0] + "_" + month + "/" + fileNamex[0] + "_" + str(count) + '.jpg', 'JPEG', quality=95)
                    else:
                        imag.save(destiny_path + fileNamex[0] + "_" + month + "/" + fileNamex[0] + "_" + str(count) + '.jpg', 'JPEG', quality=95)
                    catalogList.append(destiny_path + fileNamex[0] + "_" + month + "/" + fileNamex[0] + "_" + str(count) + '.jpg')
            else:
                cicle = round(len(images) / 50) + 1
                start = 0
                stop = 50
                while cicle:
                    pages = convert_from_path(origen_path + nameFile, dpi=800, size=(1000, None), fmt="jpeg", output_folder=destiny_path + fileNamex[0] + "_" + month + "/", output_file=fileNamex[0] + "_" + str(count) + '.jpg', first_page=start, last_page=stop)
                    start += 51
                    stop += 51
                    cicle -= 1
                for pdf in os.listdir(destiny_path + fileNamex[0] + "_" + month + "/"):
                    jpgfile = destiny_path + fileNamex[0] + "_" + month + "/" + pdf
                    catalogList.append(jpgfile)
                    catalog = fileNamex[0]
            goDrive(catalog, catalogList)
            return redirect('/pdfTool')

        if user_answer == "Compu":
            crearFolder(destiny_path, fileNamex, month)
            if len(images) <= 100:
                for imag in images:
                    count += 1
                    if imag.width > 1000:
                        new_img = (1000, None)
                        imag.save(destiny_path + fileNamex[0] + "_" + month + "/" + fileNamex[0] + "_" + str(count) + '.jpg', 'JPEG', quality=95)
                    else:
                        imag.save(destiny_path + fileNamex[0] + "_" + month + "/" + fileNamex[0] + "_" + str(count) + '.jpg', 'JPEG', quality=95)
            else:
                cicle = round(len(images) / 50) + 1
                start = 0
                stop = 50
                while cicle:
                    pages = convert_from_path(origen_path + nameFile, dpi=800, size=(1000, None), fmt="jpeg", output_folder=destiny_path + fileNamex[0] + "_" + month + "/", output_file=fileNamex[0] + "_" + str(count) + '.jpg', first_page=start, last_page=stop)
                    start += 51
                    stop += 51
                    cicle -= 1
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
