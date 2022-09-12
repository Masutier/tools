from django.urls import path, include
from .views import *

urlpatterns = [
    path('xlsTool', xlsTool, name="xlsTool"),
    path('excelTable', excelTable, name="excelTable"),
    path('duplicates', duplicates, name="duplicates"),
    path('createNewXls', createNewXls, name="createNewXls"),
    path('createAddXls', createAddXls, name="createAddXls"),
    path('delXls', delXls, name="delXls"),
    path('delColXls', delColXls, name="delColXls"),

]
