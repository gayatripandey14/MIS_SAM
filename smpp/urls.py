
from django.urls import path
from .views import   *

urlpatterns = [
    path("route/",RouteCreateView.as_view()),
    path("smppusers/",SmppUsersGetView.as_view()),

]