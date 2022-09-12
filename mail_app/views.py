from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
#mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mailTool(request):

    context = {'title':'Email'}
    return render(request, 'mail_app/mailTool.html', context)


def mailSend(request):
    subject = 'Tu orden # ' + '1254' + ' ya esta en ruta'
    html_message = render_to_string(
        'mail_app/correoSend.html',
        context={
        "name": 'Gabriel Masutier',
        "orden": '1254',
        "Repartidor1": 'Miguel',
        "Repartidor2": 'Perez',
        "tydoc": 'Cedula Ciudadania',
        "cedulaId": '1101563254',
        }
    )
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = ["masutier@gmail.com"]
    mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)

    messages.info(request, 'Email enviado')
    return redirect('home')

#    html_message = render_to_string(
#         'mail_app/correoSend.html',
#         context={
#         "name": order.customer.name,
#         "orden": order.id,
#         "Repartidor1": order.repartidor.name,
#         "Repartidor2": order.repartidor.last_name,
#         "tydoc": order.repartidor.tydoc,
#         "cedulaId": order.repartidor.cedulaId,
#         }
#     )
