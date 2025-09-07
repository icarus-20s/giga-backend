import os
import uuid
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def send_email(context):
    try:
        
        html_content = render_to_string(context.get('template_name'), context)
        email = EmailMessage(
            subject=context.get('subject'),
            body=html_content,
            from_email=f"Giga Infosoft ",
            to=context.get('to_emails')
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

def upload_notice_pdf(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join('notices/', new_filename)
