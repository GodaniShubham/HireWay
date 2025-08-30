from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

User = get_user_model()
from .models import UserProfile

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")
        roll_number = request.POST.get("roll_number")
        branch = request.POST.get("branch")
        graduation_year = request.POST.get("graduation_year")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("accounts:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("accounts:register")

        # Create user in Django's default User table
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create profile in our custom table
        UserProfile.objects.create(
            user=user,
            role=role,
            roll_number=roll_number,
            branch=branch,
            graduation_year=graduation_year
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html")

# ------------------ LOGIN ------------------
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile

from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserProfile

from django.contrib.auth import authenticate, login
from django.contrib import messages
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        role = request.POST.get("role")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Find user by email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return render(request, "accounts/login.html", {"email": email})

        # Authenticate using username + password (Django needs username)
        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            # Logged in successfully
            login(request, user)

            # Fetch role from UserProfile
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                messages.error(request, "Profile not found.")
                return render(request, "accounts/login.html")

            if profile.role != role:
                messages.error(request, "Selected role does not match your account role.")
                return render(request, "accounts/login.html", {"email": email})

            # Redirect based on role
            if profile.role == "student":
                return redirect("student_dashboard")
            elif profile.role == "company":
                return redirect("company_dashboard")
            elif profile.role == "tpo":
                return redirect("tpo_dashboard")

        else:
            messages.error(request, "Invalid password.")

    return render(request, "accounts/login.html")

# -----------
# ------------------ LOGOUT ------------------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


# ------------------ PROFILE ------------------
@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


# ------------------ DASHBOARD ------------------
@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")


# ------------------ FORGOT PASSWORD ------------------
def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("accounts:forgot_password")

        # Generate reset link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(
            reverse("accounts:reset_password", kwargs={"uidb64": uid, "token": token})
        )

        # Send email
        subject = "Password Reset Request"
        message = render_to_string("accounts/password_reset_email.html", {
            "user": user,
            "reset_link": reset_url,
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        messages.success(request, "Password reset link sent to your email.")
        return redirect("accounts:login")

    return render(request, "accounts/forgot_password.html")


# ------------------ RESET PASSWORD ------------------
def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect(request.path)

            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful! You can log in now.")
            return redirect("accounts:login")

        return render(request, "accounts/reset_password.html", {"validlink": True})
    else:
        messages.error(request, "Invalid or expired password reset link.")
        return redirect("accounts:forgot_password")


def student_dashboard(request):
    return render(request, "student_dashboard.html")

def company_dashboard(request):
    return render(request, "company_dashboard.html")

def tpo_dashboard(request):
    return render(request, "tpo_dashboard.html")
