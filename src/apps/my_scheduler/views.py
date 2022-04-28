import imp
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from lms import settings

def send_due_date_mail(x):
    content = {
        'full_name': x.user.user.first_name + ' ' + x.user.user.last_name,
        'list_book': x.borrows.all(),
    }
    html_content = render_to_string('due_date_notification.html', content)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        "Waktu peminjaman hampir habis",
        text_content,
        settings.EMAIL_HOST_USER,
        [x.user.user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()