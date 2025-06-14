from django.shortcuts import render
import logging
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import os
import tempfile
import requests

logger = logging.getLogger(__name__)

def send_user_message(recipient, message, choice):
    if not recipient or not message or not choice:
        logger.warning("Missing recipient, message, or choice.")
        return "❌ Please provide recipient, message, and choice."

    if choice == 'email':
        try:
            send_mail(
                'Message from Django App',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient],
                fail_silently=False,
            )
            logger.info(f"Email sent to {recipient}")
            return "✅ Email sent!"
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return f"❌ Email sending failed: {e}"
    elif choice == 'whatsapp':
        try:
            url = settings.WHATSAPP_API_URL
            headers = {
                "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            }
            data = {
                "messaging_product": "whatsapp",
                "to": recipient,
                "type": "text",
                "text": {"body": message}
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"WhatsApp message sent to {recipient}")
                return "✅ WhatsApp message sent!"
            else:
                logger.error(f"WhatsApp sending failed: {response.text}")
                return f"❌ WhatsApp sending failed: {response.text}"
        except Exception as e:
            logger.error(f"WhatsApp sending failed: {e}")
            return f"❌ WhatsApp sending failed: {e}"
    else:
        logger.warning(f"Invalid choice: {choice}")
        return "❌ Invalid option"

def send_pdf(recipient, pdf_path, choice, subject="PDF Document", body="Please find the attached PDF."):
    if not recipient or not pdf_path or not choice:
        return "❌ Please provide recipient, PDF path, and choice."

    if choice == 'email':
        if not os.path.exists(pdf_path):
            return "❌ PDF file does not exist."
        try:
            email = EmailMessage(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [recipient],
            )
            email.attach_file(pdf_path)
            email.send(fail_silently=False)
            return "✅ Email with PDF sent!"
        except Exception as e:
            return f"❌ Email sending failed: {e}"

    elif choice == 'whatsapp':
        try:
            url = settings.WHATSAPP_API_URL
            headers = {
                "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            }
            # pdf_path must be a public URL for WhatsApp
            data = {
                "messaging_product": "whatsapp",
                "to": recipient,
                "type": "document",
                "document": {
                    "link": pdf_path,
                    "caption": body
                }
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200 or response.status_code == 201:
                return "✅ WhatsApp PDF sent!"
            else:
                return f"❌ WhatsApp sending failed: {response.text}"
        except Exception as e:
            return f"❌ WhatsApp sending failed: {e}"

    else:
        return "❌ Invalid option"

def send_message(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        recipient = request.POST.get('recipient')
        action = request.POST.get('action')

        if action == 'message':
            message = request.POST.get('message')
            status = send_user_message(recipient, message, choice)
        elif action == 'pdf':
            if choice == 'whatsapp':
                pdf_url = request.POST.get('pdf_url')
                if not pdf_url or not pdf_url.lower().endswith('.pdf'):
                    status = "❌ Please provide a valid public PDF URL for WhatsApp."
                else:
                    status = send_pdf(recipient, pdf_url, choice)
            else:
                uploaded_file = request.FILES.get('pdf_file')
                if not uploaded_file or not uploaded_file.name.endswith('.pdf'):
                    status = "❌ Please upload a valid PDF file."
                else:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                        for chunk in uploaded_file.chunks():
                            tmp.write(chunk)
                        tmp_path = tmp.name
                    status = send_pdf(recipient, tmp_path, choice)
                    os.remove(tmp_path)
        else:
            status = "❌ Invalid action."

        return render(request, 'messageapp/form.html', {'status': status})

    return render(request, 'messageapp/form.html')
