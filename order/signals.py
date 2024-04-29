from django.dispatch import receiver
from django.core.mail import send_mail
from project.settings import EMAIL_HOST_USER
from .services import order_confirmed


@receiver(order_confirmed)
def send_order_confirmation_email(sender, order, **kwargs):
    subject = "Order Confirmation Email"
    message = f"Dear {order.user.username} your order {order.uuid} has been confirmed, thank you for your patronage."
    recipient_email = "riashadhassan1@gmail.com"
    try:
        send_mail(subject, message, EMAIL_HOST_USER, [recipient_email])
    except:
        print("unsuccessful send")
