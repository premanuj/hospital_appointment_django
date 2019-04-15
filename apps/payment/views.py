from django.urls import reverse
from django.conf import settings
from apps.appointment.models import Appointment
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from apps.profile.models import Patient
from .forms import CheckoutForm
from django.shortcuts import render, redirect
from apps.payment.models import Payment


# Create your views here.


def checkout(request, id):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            request.session["appointment_fee"] = request.POST.get("appointment_fee")
            request.session["appointment_id"] = id
            return redirect("process_payment")
    form = CheckoutForm()
    return render(request, "payment/checkout.html", {"form": form})


def process_payment(request):
    user = request.user
    appointment_id = request.session["appointment_id"]
    patient = get_object_or_404(Patient, user=user.id)
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": request.session["appointment_fee"],
        "item_name": "Order {}".format(appointment.id),
        "invoice": str(appointment.id),
        "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
        "return_url": "http://{}{}".format(host, reverse("payment_done")),
        "cancel_return": "http://{}{}".format(host, reverse("payment_cancelled")),
    }

    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(
        request, "payment/process_payment.html", {"appointment": appointment, "form": form}
    )


def payment_done(request):
    appointment_id = request.session["appointment_id"]
    payment = Payment.objects.get(appointment=appointment_id)
    payment.status = True
    payment.save()
    return render(request, "payment/payment_done.html")


def payment_canceled(request):
    return render(request, "payment/payment_cancelled.html")

