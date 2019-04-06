from django.urls import reverse
from django.conf import settings
from apps.appointment import Appointment
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def process_payment(request):
    user = request.user
    appointment = get_object_or_404(Appointment, id=user.id)
    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": 100,
        "item_name": "Order {}".format(appointment.id),
        "invoice": str(appointment.id),
        "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
        "return_url": "http://{}{}".format(host, reverse("payment_done")),
        "cancel_return": "http://{}{}".format(host, reverse("payment_cancelled")),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(
        request, "ecommerce_app/process_payment.html", {"appointment": appointment, "form": form}
    )


def payment_done(request):
    return render(request, "ecommerce_app/payment_done.html")


def payment_canceled(request):
    return render(request, "ecommerce_app/payment_cancelled.html")

