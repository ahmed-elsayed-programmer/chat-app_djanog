from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings

from account.forms import AccoountAuthenticationForm, RegistrationForm
from .models import Account


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email").lower()
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("home")
        else:
            context["registration_form"] = form

    else:
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "account/register.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccoountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)

                return redirect("home")
        else:
            context["login_form"] = form
    return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))

    return redirect


def account_view(request, id):

    context = {}
    try:
        account = Account.objects.get(pk=id)
    except:
        return HttpResponse("That user doesn't exist. ")

    if account:
        context["user_id"] = account.id
        context["username"] = account.username
        context["email"] = account.email
        context["profile_image"] = account.profie_image.url
        context["hide_email"] = account.hide_email
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        context["is_self"] = is_self
        context["is_friend"] = is_friend
        context["BASE_URL"] = settings.BASE_URL

        return render(request, "account/account.html", context)


def account_search_view(request):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = (
                Account.objects.filter(email__icontains=search_query)
                .filter(username__icontains=search_query)
                .distinct()
            )
            user = request.user
            accounts = []  # [(account1, True), (account2, False), ...]
            for account in search_results:
                accounts.append((account, False))  # you have no friends yet
            context["accounts"] = accounts

    return render(request, "account/search_results.html", context)
