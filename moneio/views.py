import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Account, MoneyInOut


def check_login(func):
  def views(request):

    # Authenticated users view their dashbord
    if request.user.is_authenticated:
      accounts = Account.objects.filter(user = request.user)
      breakdowns = MoneyInOut.objects.filter(user = request.user)
      accounts = [account.serialize() for account in accounts]
      breakdowns = [breakdown.serialize() for breakdown in breakdowns]

      # Calculate current balance for each account
      for breakdown in breakdowns:
        for account in accounts:
          if account["name"] == breakdown["account"] and not breakdown["is_deductible"]:
            account["balance"] += breakdown["price"]

      # Calculate current overall total balances
      current_total_balance = 0
      current_total_floating = 0
      current_total_deductibles = 0
      for account in accounts:
        if account["is_floating"]:
          current_total_floating += account["balance"]
        else:
          current_total_balance += account["balance"]
      for breakdown in breakdowns:
        if breakdown["is_deductible"]:
          current_total_deductibles += breakdown["price"]

      # Separate deductibles from normal breakdowns
      breakdowns_normal = []
      breakdowns_deductibles = []
      for breakdown in breakdowns:
        if breakdown["is_deductible"]:
          breakdowns_deductibles.append(breakdown)
        else:
          breakdowns_normal.append(breakdown)

      # Calculate current total gross, net, and on hand
      current_total_gross = current_total_balance + current_total_floating
      current_total_net = current_total_gross - current_total_deductibles
      current_total_onhand = current_total_net - current_total_floating
      return render(request, "moneio/index.html", {
        "data": {
          "accounts": accounts,
          "breakdowns_normal": breakdowns_normal,
          "breakdowns_deductibles": breakdowns_deductibles,
          "current_total_balance": current_total_balance,
          "current_total_floating": current_total_floating,
          "current_total_gross": current_total_gross,
          "current_total_deductible": current_total_deductibles,
          "current_total_net": current_total_net,
          "current_total_onhand": current_total_onhand,
        },
      })
    return func(request)
  return views


# Create your views here.
@check_login
def index(request):

  # Everyone is prompted to sign in
  return HttpResponseRedirect(reverse("login"))


@check_login
def login_view(request):
  if request.method == "POST":

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
    else:
      return render(request, "moneio/login.html", {
        "message": "Invalid username and/or password."
      })
  else:
    return render(request, "moneio/login.html")


def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))


@check_login
def register(request):
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    if password != confirmation:
      return render(request, "moneio/register.html", {
        "message": "Passwords must match."
      })

    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      user.save()
    except IntegrityError:
      return render(request, "moneio/register.html", {
        "message": "Username already taken."
      })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))
  else:
    return render(request, "moneio/register.html")


@csrf_exempt
@login_required
def account(request):

  # Add account
  if request.method == "POST":
    data = json.loads(request.body)
    new_account = Account(
      user = request.user,
      name = data.get("name"),
      initial_balance = data.get("balance"),
      initial_balance_date = data.get("date"),
      is_floating = data.get("isFloating"),
    )
    new_account.save()
    return HttpResponse(status=204)
  return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def moneio(request):

  # Add money in/money out
  if request.method == "POST":
    data = json.loads(request.body)
    signed_price = float(data.get("money"))

    # Convert if money out to negative value
    if not data.get("isMoneyIn"):
      signed_price = signed_price * (-1)
    new_breakdown = MoneyInOut(
      user = request.user,
      name = data.get("name"),
      price = signed_price,
      date = data.get("date"),
      is_deductible = False,
      account = Account.objects.get(user = request.user, name = data.get("account"))
    )
    new_breakdown.save()
  return HttpResponseRedirect(reverse("index"))
