from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_completion_email(user,email):
    send_mail(
        subject="Order Recieved",
        message="Dear User,Your Order Process is completed make your payment and the delivery will be on your way.",
    from_email="",
    recipient_list=[email],
    fail_silently=False
    )