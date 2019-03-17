from django.urls import path, re_path
from django.contrib.auth import views
from .views import UserSignUp, UserAccountActivationSent, user_activate


urlpatterns = [
    path("register/", UserSignUp.as_view(), name="register"),
    path("login/", views.LoginView.as_view(template_name="profile/login.html"), name="login"),
    path("logout/", views.LogoutView.as_view(template_name="profile/logout.html"), name="logout"),
    path(
        "password-reset/",
        views.PasswordResetView.as_view(
            template_name="profile/password_reset_form.html",
            email_template_name="profile/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path("password-reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="profile/password_reset_conformation_form.html", success_url="/"
        ),
        name="password_reset_confirm",
    ),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("account-activation-sent/", UserAccountActivationSent.as_view(), name="account_activation_sent"),
    re_path(r'^account-activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user_activate, name="account-activation"),
]
