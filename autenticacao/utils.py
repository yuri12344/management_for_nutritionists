import re
from django import conf
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def password_is_valid(request, password, confirm_password):
    if len(password) < 2:
        messages.add_message(request, constants.ERROR, 'Password must be at least 8 characters long.')
        return False
    """
    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'Passwords do not match.')
        return False
    
    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Password must contain at least one uppercase letter.')
        return False

    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Password must contain at least one lowercase letter.')
        return False
    
    if not re.search(['1-9'], password):
        messages.add_message(request, constants.ERROR, 'Password must contain at least one number.')

        return False
    """
    return True


def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)
    
    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}