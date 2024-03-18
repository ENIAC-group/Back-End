from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from BackEnd.settings import EMAIL_HOST
from . import project_variables
import json


def send_verification_message(subject, recipient_list, verification_token, registration_tries, show_text , token):
    # remaining_registration_tries = project_variables.MAX_VERIFICATION_TRIES - registration_tries
    

    context = {
        'email_verification_token': verification_token,
        # 'remaining_text': remaining_text,
        'varification_link' : token ,
    }

    html_message = render_to_string( 'active_email.html', context=  context  )  #'activation_template.html'
    email = EmailMultiAlternatives(subject, '', EMAIL_HOST, recipient_list)
    email.attach_alternative(html_message, "text/html" )  #"text/html")
    email.send()


def send_forget_password_verification_message(subject, recipient_list, verification_token, verification_tries):
    remaining_verification_tries = project_variables.MAX_VERIFICATION_TRIES - verification_tries
    if remaining_verification_tries < project_variables.MAX_VERIFICATION_TRIES:
        remaining_text = f'تا کنون به تعداد {verification_tries}بار، ' \
                         f'درخواست تغییر رمز عبور داشته اید. به تعداد {remaining_verification_tries} ' \
                         f'دفعۀ دیگر می توانید برای دریافت کد تایید، درخواست نمایید. ' 
    else:
        remaining_text = 'به سقف مجاز برای ثبت درخواست کد تایید رسیده اید. ' \
                         'پس از 12 ساعت انتظار، می توانید برای باری دیگر، برای دریافت کد تایید، درخواست نمایید.'
    context = {
        'email_verification_token': verification_token,
        'remaining_text': remaining_text,
    }

    html_message = render_to_string('forget_password.html', context)
    email = EmailMultiAlternatives(subject, '', EMAIL_HOST, recipient_list)
    email.attach_alternative(html_message, "text/html")
    email.send()

