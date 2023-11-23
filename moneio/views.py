import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Account, MoneyInOut


def authenticate_index(func):
  def views(request):

    # Authenticated users view their dashboard
    if request.user.is_authenticated:

      # Get list of user's accounts alphabetically and money in/money out reverse chronologically
      accounts = Account.objects.filter(user = request.user).order_by("name")
      breakdowns = MoneyInOut.objects.filter(user = request.user).order_by("-date")
      accounts = [account.serialize() for account in accounts]
      breakdowns = [breakdown.serialize() for breakdown in breakdowns]

      # Calculate current balance for each account
      for breakdown in breakdowns:
        for account in accounts:
          if account["name"] == breakdown["account"]:
            account["balance"] += breakdown["price"]

      # Calculate current overall total balances
      current_total_balance = 0
      current_total_floating = 0
      current_total_deductibles = 0
      for account in accounts:
        if account["is_floating"]:
          if account["balance"] >= 0:
            current_total_floating += account["balance"]
          else:
            current_total_deductibles += account["balance"]
        else:
          current_total_balance += account["balance"]

      # Convert deductibles to positive for display
      current_total_deductibles = current_total_deductibles * (-1)

      # Calculate current total gross, net, and on hand
      current_total_gross = current_total_balance + current_total_floating
      current_total_net = current_total_gross - current_total_deductibles
      current_total_onhand = current_total_net - current_total_floating
      return render(request, "moneio/index.html", {
        "data": {
          "accounts": accounts,
          "breakdowns": breakdowns,
          "current_total_balance": current_total_balance,
          "current_total_floating": current_total_floating,
          "current_total_gross": current_total_gross,
          "current_total_deductibles": current_total_deductibles,
          "current_total_net": current_total_net,
          "current_total_onhand": current_total_onhand,
        },
      })
    return func(request)
  return views


# Create your views here.
@authenticate_index
def index(request):

  # Everyone is prompted to sign in
  return HttpResponseRedirect(reverse("login"))


@authenticate_index
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
        "message": "Invalid username and/or password.",
      })
  else:
    return render(request, "moneio/login.html")


def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))


@authenticate_index
def register(request):
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    if password != confirmation:
      return render(request, "moneio/register.html", {
        "message": "Passwords must match.",
      })

    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      user.save()
    except IntegrityError:
      return render(request, "moneio/register.html", {
        "message": "Username already taken.",
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

    # Add new account
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
    account_name = data.get("account")
    signed_price = float(data.get("money"))

    # Convert if money out to negative value
    if not data.get("isMoneyIn"):
      signed_price = signed_price * (-1)

    # Get list of user's accounts and money in/money out
    accounts = Account.objects.filter(user = request.user)
    breakdowns = MoneyInOut.objects.filter(user = request.user)
    accounts = [account.serialize() for account in accounts]
    breakdowns = [breakdown.serialize() for breakdown in breakdowns]

    # Calculate current balance for each account
    for breakdown in breakdowns:
      for account in accounts:
        if account["name"] == breakdown["account"]:
          account["balance"] += breakdown["price"]

    # Reverse sign if account chosen is a deductibles account
    for account in accounts:
      if account["name"] == account_name and account["is_floating"] and account["balance"] < 0:
        signed_price = signed_price * (-1)

    # Add new money in/money out
    new_breakdown = MoneyInOut(
      user = request.user,
      name = data.get("name"),
      price = signed_price,
      date = data.get("date"),
      account = Account.objects.get(user = request.user, name = account_name)
    )
    new_breakdown.save()
  return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def edit_account(request, username, account_id):

  # Check if param is the current logged in user
  if (request.user.username != username):
    return HttpResponseRedirect(reverse("index"))
  
  # Check if the logged in user owns the account
  account = Account.objects.filter(pk = account_id, user = request.user)
  if not account:
    return HttpResponseRedirect(reverse("index"))
  
  # Edit account details
  if request.method == "PUT":
    data = json.loads(request.body)
    account[0].name = data.get("name")
    account[0].initial_balance = data.get("balance")
    account[0].initial_balance_date = data.get("date")
    account[0].save()
    return HttpResponse(status=204)

  # Delete account
  if request.method == "DELETE":
    account.delete()
    return HttpResponse(status=204)
  return render(request, "moneio/account.html", {
    "account": account[0],
    "date": account[0].initial_balance_date.strftime("%Y-%m-%d"),
  })


@csrf_exempt
@login_required
def edit_account_deductibles(request, username, account_id):

  # Check if param is the current logged in user
  if (request.user.username != username):
    return HttpResponseRedirect(reverse("index"))
  
  # Check if the logged in user owns the account
  account = Account.objects.filter(pk = account_id, user = request.user)
  if not account:
    return HttpResponseRedirect(reverse("index"))
  
  # Edit account details
  if request.method == "PUT":
    data = json.loads(request.body)
    account[0].name = data.get("name")
    account[0].initial_balance = float(data.get("balance")) * (-1) # Convert to negative for storing value in deductibles
    account[0].initial_balance_date = data.get("date")
    account[0].save()
    return HttpResponse(status=204)

  # Delete account
  if request.method == "DELETE":
    account.delete()
    return HttpResponse(status=204)
  account[0].initial_balance = account[0].initial_balance * (-1) # Convert to positive for display
  return render(request, "moneio/account.html", {
    "account": account[0],
    "date": account[0].initial_balance_date.strftime("%Y-%m-%d"),
  })
