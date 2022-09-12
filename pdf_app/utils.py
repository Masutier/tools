import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def render_to_pdf(template_src, context_dic={}):
    template = get_template(template_src)
    html = template.render(context_dic)
    result = BytesIO()
    pdf= pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def crearFolder(destiny_path, fileNamex, month):
    os.makedirs(destiny_path + fileNamex[0] + "_" + month)
    endDir = destiny_path + fileNamex[0] + "_" + month
    return endDir


def goDrive(catalog, catalogList):
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile('settings.yaml')
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    count = 0
    for upload_file in catalogList:
        count += 1
        gfile = drive.CreateFile({'parents': [{'id': catalog}]})
        gfile.SetContentFile(upload_file)
        gfile.Upload()
    gfile.content.close()
    return
