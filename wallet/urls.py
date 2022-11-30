from django.urls import path
from .views import   *

urlpatterns = [
    path("balance/", GetWalletView.as_view()),
]