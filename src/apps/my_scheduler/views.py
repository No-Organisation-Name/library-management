import imp
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from lms import settings

def send_due_date_mail(transaction):
    content = {
        'full_name': transaction.user.user.first_name + ' ' + transaction.user.user.last_name,
        'list_book': transaction.borrows.all(),
    }
    html_content = render_to_string('due_date_notification.html', content)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        "Waktu peminjaman hampir habis",
        text_content,
        settings.EMAIL_HOST_USER,
        [transaction.user.user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_fine_notification_mail(transaction):
    content = {
        'full_name':transaction.user.user.first_name + ' ' + transaction.user.user.last_name,
        'fine':transaction.fine,
        'list_book':transaction.borrows.all(),

    }
    html_content = render_to_string('fine_notification.html', content)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        "Peringatan denda",
        text_content,
        settings.EMAIL_HOST_USER,
        [transaction.user.user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    