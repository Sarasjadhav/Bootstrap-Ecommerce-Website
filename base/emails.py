from django.core.mail import send_mail
from django.conf import settings

def send_account_activation_email(email_token,email):
    subject='Your account needs to be verified'
    message=f'Click on the link to verify your account http://127.0.0.1:8000/accounts/activate/{email_token}/'
    email_from=settings.EMAIL_HOST_USER
        # Print debug info
    print(f"Sending email to: {email}")
    print(f"Email content: {message}")
    send_mail(subject,message,email_from,[email])
    
    
    
    