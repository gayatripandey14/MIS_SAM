from django.urls import path
from .views import   *

urlpatterns = [
    path("get-usernames/", GetChildrensView.as_view()),
    path("sms-log", SmsLogView.as_view()),
    path("analytics-customer", CustomerAnalyticsView.as_view()),
    path("analytics-route", RouteAnalyticsView.as_view()),
    path("smsc-list", SmscListVIEW.as_view()),
    path("children-under-me", GetChildrensUnderMeView.as_view()),



]