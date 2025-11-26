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

@shared_task
def order_confirmed_email(user,email):
    send_mail(
        subject="Order Confirmed",
        message="Dear User,Your Order is confirmed our delivery partners will be getting your package soon.",
    from_email="",
    recipient_list=[email],
    fail_silently=False
    )

@shared_task
def delivery_completed(user,email):
    send_mail(
        subject="Order Confirmed",
        message="Dear User,Your Delivery is Completed,Thank You for choosing us.",
    from_email="",
    recipient_list=[email],
    fail_silently=False
    )

@shared_task
def order_cancelled(user,email):
    send_mail(
        subject="Order Confirmed",
        message="The Order assigned to you has been cancelled please wait for another order to be assigned.",
    from_email="",
    recipient_list=[email],
    fail_silently=False
    )