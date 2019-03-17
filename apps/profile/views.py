from .models import User
from django.views import View
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.views.generic.base import RedirectView
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class UserSignUp(View):
    singnup_template = "profile/signup.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.singnup_template, {"form": form})

    def post(self, request):
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.role = 1  # Patient role is one
                user.save()
                current_site = get_current_site(request)
                subject = "Activate Your Appointment APP Account"
                message = render_to_string(
                    "profile/account_activation_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        "token": PasswordResetTokenGenerator().make_token(user),
                    },
                )
                user.email_user(subject, message)
            else:
                return render(request, self.singnup_template, {"form": form})

            return redirect("account_activation_sent")
        else:
            form = SignUpForm()
            return render(request, self.singnup_template, {"form": form})


class UserAccountActivationSent(RedirectView):
    url = "/users/login/"


def user_activate(request, uidb64, token):
    print(uidb64, token)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and PasswordResetTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("/")
    return render(request, "profile/account_activation_invalid.html")

