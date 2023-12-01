from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("login", views.login_view, name="login"),
  path("logout", views.logout_view, name="logout"),
  path("register", views.register, name="register"),

  # API Routes
  path("account", views.account, name="account"),
  path("<str:username>/account/<int:account_id>", views.edit_account, name="edit_account"),
  path("moneio", views.moneio, name="moneio"),
  path("<str:username>/monei/<int:monei_id>", views.monei, name="monei"),
  path("<str:username>/moneo/<int:moneo_id>", views.moneo, name="moneo"),
  path("transfer", views.transfer, name="transfer"),
  path("<str:username>/transfer/<int:transfer_id>", views.edit_transfer, name="edit_transfer"),
]
