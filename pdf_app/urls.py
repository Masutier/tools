from django.urls import path, include
from .views import *

urlpatterns = [
    path('pdfTool', pdfTool, name="pdfTool"),
    path('pdfLoad', pdfLoad, name="pdfLoad"),

    path('createPdf', createPdf, name="createPdf"),
    path('ordenCompraDownloadPDF', ordenCompraDownloadPDF, name="ordenCompraDownloadPDF"),

]
